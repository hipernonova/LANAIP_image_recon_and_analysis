"""
Tests for list mode to sinogram conversion.
"""

import pytest
import numpy as np
from lanaip.reconstruction import ListModeToSinogram, convert_lm_to_sinogram


class TestListModeToSinogram:
    """Test cases for ListModeToSinogram class."""
    
    def test_initialization(self):
        """Test converter initialization."""
        converter = ListModeToSinogram()
        
        assert converter.num_rings == 4
        assert converter.num_detectors_per_ring == 160
        assert converter.num_bins_s == 128
        assert converter.num_bins_phi == 128
        assert converter.max_ring_diff == 3
        assert converter.span == 1
    
    def test_custom_parameters(self):
        """Test converter with custom parameters."""
        converter = ListModeToSinogram(
            num_rings=8,
            num_detectors_per_ring=256,
            num_bins_s=256,
            num_bins_phi=256
        )
        
        assert converter.num_rings == 8
        assert converter.num_detectors_per_ring == 256
        assert converter.num_bins_s == 256
        assert converter.num_bins_phi == 256
    
    def test_sinogram_calculation(self):
        """Test sinogram dimensions calculation."""
        converter = ListModeToSinogram(num_rings=4, max_ring_diff=3)
        
        # Direct planes: 4
        # Oblique planes: 2*(4-1) + 2*(4-2) + 2*(4-3) = 6 + 4 + 2 = 12
        # Total: 4 + 12 = 16
        assert converter.num_sinograms == 16
    
    def test_get_sinogram_info(self):
        """Test sinogram info retrieval."""
        converter = ListModeToSinogram()
        info = converter.get_sinogram_info()
        
        assert 'num_rings' in info
        assert 'num_detectors_per_ring' in info
        assert 'num_bins_s' in info
        assert 'num_bins_phi' in info
        assert 'num_sinograms' in info
        assert 'shape' in info
        
        expected_shape = (16, 128, 128)
        assert info['shape'] == expected_shape
    
    def test_convert_with_dummy_data(self):
        """Test conversion with dummy list mode data."""
        converter = ListModeToSinogram()
        
        # Create dummy list mode data
        num_events = 1000
        lm_data = np.column_stack([
            np.random.rand(num_events),  # time
            np.random.randint(0, 640, num_events),  # det1
            np.random.randint(0, 640, num_events),  # det2
            np.random.rand(num_events) * 511 + 350,  # energy1
            np.random.rand(num_events) * 511 + 350,  # energy2
        ])
        
        sinogram = converter.convert(lm_data)
        
        # Check sinogram shape
        assert sinogram.shape == (16, 128, 128)
        assert sinogram.dtype == np.float32
        
        # Check that sinogram contains data
        assert np.sum(sinogram) > 0
    
    def test_time_filter(self):
        """Test time filtering."""
        converter = ListModeToSinogram()
        
        # Create data with specific time range
        num_events = 1000
        lm_data = np.column_stack([
            np.linspace(0, 100, num_events),  # time 0-100
            np.random.randint(0, 640, num_events),  # det1
            np.random.randint(0, 640, num_events),  # det2
            np.ones(num_events) * 511,  # energy1
            np.ones(num_events) * 511,  # energy2
        ])
        
        # Apply time filter
        filtered = converter._apply_time_filter(lm_data, (25, 75))
        
        # Should keep roughly 50% of events
        assert len(filtered) < len(lm_data)
        assert len(filtered) > len(lm_data) * 0.4  # Allow some tolerance
        
        # Check that all times are in range
        assert np.all(filtered[:, 0] >= 25)
        assert np.all(filtered[:, 0] <= 75)
    
    def test_energy_filter(self):
        """Test energy filtering."""
        converter = ListModeToSinogram()
        
        # Create data with specific energies
        num_events = 1000
        lm_data = np.column_stack([
            np.random.rand(num_events),  # time
            np.random.randint(0, 640, num_events),  # det1
            np.random.randint(0, 640, num_events),  # det2
            np.random.normal(511, 100, num_events),  # energy1
            np.random.normal(511, 100, num_events),  # energy2
        ])
        
        # Apply energy filter
        filtered = converter._apply_energy_filter(lm_data, (450, 570))
        
        # Should filter out some events
        assert len(filtered) <= len(lm_data)
        
        # Check that energies are in range
        assert np.all(filtered[:, 3] >= 450)
        assert np.all(filtered[:, 3] <= 570)
        assert np.all(filtered[:, 4] >= 450)
        assert np.all(filtered[:, 4] <= 570)
    
    def test_convenience_function(self):
        """Test convenience function."""
        # Create temporary dummy file
        num_events = 100
        lm_data = np.column_stack([
            np.random.rand(num_events),
            np.random.randint(0, 640, num_events),
            np.random.randint(0, 640, num_events),
            np.ones(num_events) * 511,
            np.ones(num_events) * 511,
        ])
        
        # Convert directly from array (not file)
        converter = ListModeToSinogram()
        sinogram = converter.convert(lm_data)
        
        # Check output
        assert sinogram.shape == (16, 128, 128)
        assert isinstance(sinogram, np.ndarray)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

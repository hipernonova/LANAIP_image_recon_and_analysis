"""
List Mode to Sinogram Converter

This module provides functionality to convert list mode data from the 
Bruker Albira Si scanner to sinogram format for reconstruction with STIR.

Classes:
    ListModeToSinogram: Main class for list mode to sinogram conversion

Functions:
    convert_lm_to_sinogram: Convenience function for quick conversion
"""

import numpy as np
import logging
from typing import Optional, Tuple, Union
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ListModeToSinogram:
    """
    Convert list mode data to sinogram format.
    
    This class handles the conversion of list mode acquisition data from the
    Bruker Albira Si scanner to sinogram format suitable for reconstruction.
    
    Attributes:
        num_rings (int): Number of detector rings
        num_detectors_per_ring (int): Number of detectors per ring
        num_bins_s (int): Number of sinogram bins (radial)
        num_bins_phi (int): Number of angular bins
        max_ring_diff (int): Maximum ring difference to include
        span (int): Axial compression factor
    """
    
    def __init__(
        self,
        num_rings: int = 4,
        num_detectors_per_ring: int = 160,
        num_bins_s: int = 128,
        num_bins_phi: int = 128,
        max_ring_diff: int = 3,
        span: int = 1
    ):
        """
        Initialize the ListModeToSinogram converter.
        
        Args:
            num_rings: Number of detector rings (default: 4 for Albira Si)
            num_detectors_per_ring: Number of detectors per ring (default: 160)
            num_bins_s: Number of radial sinogram bins (default: 128)
            num_bins_phi: Number of angular bins (default: 128)
            max_ring_diff: Maximum ring difference to include (default: 3)
            span: Axial compression factor (default: 1)
        """
        self.num_rings = num_rings
        self.num_detectors_per_ring = num_detectors_per_ring
        self.num_bins_s = num_bins_s
        self.num_bins_phi = num_bins_phi
        self.max_ring_diff = max_ring_diff
        self.span = span
        
        # Calculate derived parameters
        self.num_sinograms = self._calculate_num_sinograms()
        
        logger.info(f"Initialized ListModeToSinogram converter:")
        logger.info(f"  Rings: {num_rings}, Detectors/ring: {num_detectors_per_ring}")
        logger.info(f"  Sinogram bins: {num_bins_s}x{num_bins_phi}")
        logger.info(f"  Number of sinograms: {self.num_sinograms}")
    
    def _calculate_num_sinograms(self) -> int:
        """
        Calculate the number of sinograms based on ring configuration.
        
        Returns:
            Number of sinograms
        """
        num_direct = self.num_rings
        num_oblique = 0
        
        for ring_diff in range(1, self.max_ring_diff + 1):
            num_oblique += 2 * (self.num_rings - ring_diff)
        
        return num_direct + num_oblique
    
    def convert(
        self,
        lm_data: Union[str, Path, np.ndarray],
        output_file: Optional[Union[str, Path]] = None,
        time_window: Optional[Tuple[float, float]] = None,
        energy_window: Optional[Tuple[float, float]] = None
    ) -> np.ndarray:
        """
        Convert list mode data to sinogram.
        
        Args:
            lm_data: Path to list mode file or numpy array with list mode data
            output_file: Optional output file path for sinogram (saves as .npy)
            time_window: Optional time window (start, end) in seconds
            energy_window: Optional energy window (min, max) in keV
        
        Returns:
            Sinogram as numpy array with shape (num_sinograms, num_bins_phi, num_bins_s)
        """
        # Load list mode data
        if isinstance(lm_data, (str, Path)):
            logger.info(f"Loading list mode data from {lm_data}")
            lm_array = self._load_list_mode_file(lm_data)
        else:
            lm_array = lm_data
        
        # Apply filters
        if time_window is not None:
            lm_array = self._apply_time_filter(lm_array, time_window)
        
        if energy_window is not None:
            lm_array = self._apply_energy_filter(lm_array, energy_window)
        
        # Initialize sinogram
        sinogram = np.zeros(
            (self.num_sinograms, self.num_bins_phi, self.num_bins_s),
            dtype=np.float32
        )
        
        # Perform conversion
        logger.info("Converting list mode to sinogram...")
        sinogram = self._histogram_events(lm_array, sinogram)
        
        # Save if output file specified
        if output_file is not None:
            self._save_sinogram(sinogram, output_file)
        
        logger.info(f"Conversion complete. Total counts: {np.sum(sinogram):.0f}")
        return sinogram
    
    def _load_list_mode_file(self, filepath: Union[str, Path]) -> np.ndarray:
        """
        Load list mode data from file.
        
        Args:
            filepath: Path to list mode file
        
        Returns:
            List mode data as numpy array
        
        Note:
            This is a placeholder. Actual implementation depends on 
            Bruker Albira Si list mode file format.
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"List mode file not found: {filepath}")
        
        # Placeholder: actual format depends on Bruker specifications
        # Expected columns: [time, det1, det2, energy1, energy2, ...]
        logger.warning("Using placeholder list mode loader. "
                      "Implement actual Bruker format reader.")
        
        # Return dummy data for demonstration
        num_events = 1000
        lm_data = np.column_stack([
            np.random.rand(num_events),  # time
            np.random.randint(0, self.num_detectors_per_ring * self.num_rings, num_events),  # det1
            np.random.randint(0, self.num_detectors_per_ring * self.num_rings, num_events),  # det2
            np.random.rand(num_events) * 511 + 350,  # energy1 (keV)
            np.random.rand(num_events) * 511 + 350,  # energy2 (keV)
        ])
        
        return lm_data
    
    def _apply_time_filter(
        self,
        lm_data: np.ndarray,
        time_window: Tuple[float, float]
    ) -> np.ndarray:
        """
        Filter list mode data by time window.
        
        Args:
            lm_data: List mode data array
            time_window: (start, end) time in seconds
        
        Returns:
            Filtered list mode data
        """
        start_time, end_time = time_window
        time_col = lm_data[:, 0]
        mask = (time_col >= start_time) & (time_col <= end_time)
        
        filtered = lm_data[mask]
        logger.info(f"Time filter: {len(lm_data)} -> {len(filtered)} events")
        return filtered
    
    def _apply_energy_filter(
        self,
        lm_data: np.ndarray,
        energy_window: Tuple[float, float]
    ) -> np.ndarray:
        """
        Filter list mode data by energy window.
        
        Args:
            lm_data: List mode data array
            energy_window: (min, max) energy in keV
        
        Returns:
            Filtered list mode data
        """
        min_energy, max_energy = energy_window
        
        # Assuming energy columns are at indices 3 and 4
        energy1 = lm_data[:, 3]
        energy2 = lm_data[:, 4]
        
        mask = ((energy1 >= min_energy) & (energy1 <= max_energy) &
                (energy2 >= min_energy) & (energy2 <= max_energy))
        
        filtered = lm_data[mask]
        logger.info(f"Energy filter: {len(lm_data)} -> {len(filtered)} events")
        return filtered
    
    def _histogram_events(
        self,
        lm_data: np.ndarray,
        sinogram: np.ndarray
    ) -> np.ndarray:
        """
        Histogram list mode events into sinogram bins.
        
        Args:
            lm_data: List mode data array
            sinogram: Initialized sinogram array to fill
        
        Returns:
            Filled sinogram array
        """
        # Extract detector pairs
        det1 = lm_data[:, 1].astype(int)
        det2 = lm_data[:, 2].astype(int)
        
        # Calculate LOR parameters for each event
        for i in range(len(lm_data)):
            d1, d2 = det1[i], det2[i]
            
            # Calculate ring indices
            ring1 = d1 // self.num_detectors_per_ring
            ring2 = d2 // self.num_detectors_per_ring
            
            # Calculate sinogram index
            ring_diff = abs(ring1 - ring2)
            if ring_diff > self.max_ring_diff:
                continue
            
            # Calculate angular and radial bin indices
            # This is a simplified calculation
            det1_angle = (d1 % self.num_detectors_per_ring) * 2 * np.pi / self.num_detectors_per_ring
            det2_angle = (d2 % self.num_detectors_per_ring) * 2 * np.pi / self.num_detectors_per_ring
            
            # Calculate LOR angle and radial position
            phi = (det1_angle + det2_angle) / 2
            phi_bin = int((phi / (2 * np.pi)) * self.num_bins_phi) % self.num_bins_phi
            
            # Simplified radial position (would need actual geometry)
            s = abs(det1_angle - det2_angle)
            s_bin = int((s / np.pi) * self.num_bins_s)
            s_bin = min(s_bin, self.num_bins_s - 1)
            
            # Determine sinogram plane
            sino_idx = self._get_sinogram_index(ring1, ring2)
            
            if 0 <= sino_idx < self.num_sinograms:
                sinogram[sino_idx, phi_bin, s_bin] += 1
        
        return sinogram
    
    def _get_sinogram_index(self, ring1: int, ring2: int) -> int:
        """
        Calculate sinogram index from ring pair.
        
        Args:
            ring1: First ring index
            ring2: Second ring index
        
        Returns:
            Sinogram index
        """
        ring_diff = ring2 - ring1
        
        if ring_diff == 0:
            # Direct plane
            return ring1
        elif ring_diff > 0:
            # Positive oblique
            offset = self.num_rings
            for rd in range(1, ring_diff):
                offset += 2 * (self.num_rings - rd)
            return offset + 2 * ring1
        else:
            # Negative oblique
            ring_diff = abs(ring_diff)
            offset = self.num_rings
            for rd in range(1, ring_diff):
                offset += 2 * (self.num_rings - rd)
            return offset + 2 * ring2 + 1
    
    def _save_sinogram(self, sinogram: np.ndarray, filepath: Union[str, Path]):
        """
        Save sinogram to file.
        
        Args:
            sinogram: Sinogram array
            filepath: Output file path
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Save as numpy array
        if filepath.suffix == '.npy':
            np.save(filepath, sinogram)
        else:
            np.save(filepath.with_suffix('.npy'), sinogram)
        
        logger.info(f"Sinogram saved to {filepath}")
    
    def get_sinogram_info(self) -> dict:
        """
        Get information about sinogram configuration.
        
        Returns:
            Dictionary with sinogram parameters
        """
        return {
            'num_rings': self.num_rings,
            'num_detectors_per_ring': self.num_detectors_per_ring,
            'num_bins_s': self.num_bins_s,
            'num_bins_phi': self.num_bins_phi,
            'num_sinograms': self.num_sinograms,
            'max_ring_diff': self.max_ring_diff,
            'span': self.span,
            'shape': (self.num_sinograms, self.num_bins_phi, self.num_bins_s)
        }


def convert_lm_to_sinogram(
    lm_file: Union[str, Path],
    output_file: Optional[Union[str, Path]] = None,
    **kwargs
) -> np.ndarray:
    """
    Convenience function to convert list mode to sinogram.
    
    Args:
        lm_file: Path to list mode file
        output_file: Optional output file path
        **kwargs: Additional arguments passed to ListModeToSinogram constructor
            and convert method
    
    Returns:
        Sinogram as numpy array
    
    Example:
        >>> sinogram = convert_lm_to_sinogram('data.lm', 'output.npy')
        >>> print(sinogram.shape)
        (10, 128, 128)
    """
    # Extract constructor arguments
    constructor_args = {
        'num_rings': kwargs.pop('num_rings', 4),
        'num_detectors_per_ring': kwargs.pop('num_detectors_per_ring', 160),
        'num_bins_s': kwargs.pop('num_bins_s', 128),
        'num_bins_phi': kwargs.pop('num_bins_phi', 128),
        'max_ring_diff': kwargs.pop('max_ring_diff', 3),
        'span': kwargs.pop('span', 1),
    }
    
    # Create converter
    converter = ListModeToSinogram(**constructor_args)
    
    # Convert
    sinogram = converter.convert(lm_file, output_file, **kwargs)
    
    return sinogram


if __name__ == '__main__':
    # Example usage
    print("LANAIP List Mode to Sinogram Converter")
    print("=" * 50)
    
    # Create example converter
    converter = ListModeToSinogram()
    info = converter.get_sinogram_info()
    
    print("\nSinogram Configuration:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\nTo use:")
    print("  from lanaip.reconstruction import convert_lm_to_sinogram")
    print("  sinogram = convert_lm_to_sinogram('input.lm', 'output.npy')")

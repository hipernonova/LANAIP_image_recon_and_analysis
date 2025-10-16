"""
Example: List Mode to Sinogram Conversion and Reconstruction

This example demonstrates how to convert list mode data to sinogram
and perform image reconstruction.
"""

import numpy as np
from lanaip.reconstruction import ListModeToSinogram, convert_lm_to_sinogram


def main():
    print("LANAIP Reconstruction Example")
    print("=" * 60)
    
    # Example 1: Using the convenience function
    print("\n1. Simple conversion using convenience function:")
    print("-" * 60)
    
    # This would work with actual list mode file
    # sinogram = convert_lm_to_sinogram('data.lm', 'output.npy')
    
    print("Usage: sinogram = convert_lm_to_sinogram('data.lm', 'output.npy')")
    
    # Example 2: Using the class with custom parameters
    print("\n2. Advanced conversion with custom parameters:")
    print("-" * 60)
    
    converter = ListModeToSinogram(
        num_rings=4,
        num_detectors_per_ring=160,
        num_bins_s=128,
        num_bins_phi=128,
        max_ring_diff=3
    )
    
    # Display configuration
    info = converter.get_sinogram_info()
    print("\nConverter Configuration:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Example 3: Conversion with filters
    print("\n3. Conversion with time and energy windows:")
    print("-" * 60)
    
    # Create some dummy list mode data for demonstration
    num_events = 5000
    dummy_lm_data = np.column_stack([
        np.random.rand(num_events) * 100,  # time (0-100 seconds)
        np.random.randint(0, 640, num_events),  # detector 1
        np.random.randint(0, 640, num_events),  # detector 2
        np.random.normal(511, 50, num_events),  # energy 1 (keV)
        np.random.normal(511, 50, num_events),  # energy 2 (keV)
    ])
    
    print(f"Generated {num_events} dummy list mode events")
    
    # Convert with filters
    sinogram = converter.convert(
        dummy_lm_data,
        time_window=(10, 90),      # Only use events between 10-90 seconds
        energy_window=(450, 570),   # Energy window around 511 keV
    )
    
    print(f"\nSinogram shape: {sinogram.shape}")
    print(f"Total counts: {np.sum(sinogram):.0f}")
    print(f"Max counts per bin: {np.max(sinogram):.0f}")
    print(f"Mean counts per bin: {np.mean(sinogram):.2f}")
    
    # Example 4: Save sinogram
    print("\n4. Saving sinogram:")
    print("-" * 60)
    print("To save: converter.convert(lm_data, output_file='sino.npy')")
    
    print("\n" + "=" * 60)
    print("Example complete!")


if __name__ == '__main__':
    main()

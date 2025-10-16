"""
Example: Image Analysis

This example demonstrates how to use the image analysis tools.
"""

import numpy as np
from lanaip.analysis.image_analysis import ImageAnalyzer


def main():
    print("LANAIP Image Analysis Example")
    print("=" * 60)
    
    # Create a dummy image
    print("\n1. Creating dummy image (64x64x64):")
    print("-" * 60)
    
    image_size = (64, 64, 64)
    image = np.random.rand(*image_size) * 100
    
    # Add a hot spot
    center = (32, 32, 32)
    radius = 5
    for i in range(center[0]-radius, center[0]+radius):
        for j in range(center[1]-radius, center[1]+radius):
            for k in range(center[2]-radius, center[2]+radius):
                if ((i-center[0])**2 + (j-center[1])**2 + (k-center[2])**2) <= radius**2:
                    image[i, j, k] = 500
    
    print(f"Image shape: {image.shape}")
    print(f"Image range: [{np.min(image):.2f}, {np.max(image):.2f}]")
    
    # Create ROIs
    print("\n2. Creating ROI masks:")
    print("-" * 60)
    
    # Hot spot ROI
    hot_roi = np.zeros(image_size, dtype=bool)
    for i in range(center[0]-radius, center[0]+radius):
        for j in range(center[1]-radius, center[1]+radius):
            for k in range(center[2]-radius, center[2]+radius):
                if ((i-center[0])**2 + (j-center[1])**2 + (k-center[2])**2) <= radius**2:
                    hot_roi[i, j, k] = True
    
    # Background ROI
    bg_roi = np.zeros(image_size, dtype=bool)
    bg_roi[5:15, 5:15, 5:15] = True
    
    print(f"Hot ROI voxels: {np.sum(hot_roi)}")
    print(f"Background ROI voxels: {np.sum(bg_roi)}")
    
    # Analyze
    print("\n3. ROI statistics:")
    print("-" * 60)
    
    analyzer = ImageAnalyzer()
    
    hot_stats = analyzer.calculate_roi_statistics(image, hot_roi)
    print("\nHot spot statistics:")
    for key, value in hot_stats.items():
        print(f"  {key}: {value:.2f}")
    
    bg_stats = analyzer.calculate_roi_statistics(image, bg_roi)
    print("\nBackground statistics:")
    for key, value in bg_stats.items():
        print(f"  {key}: {value:.2f}")
    
    # Calculate contrast
    print("\n4. Contrast calculation:")
    print("-" * 60)
    
    contrast = analyzer.calculate_contrast(image, hot_roi, bg_roi)
    print(f"Contrast: {contrast:.2f}")
    
    print("\n" + "=" * 60)
    print("Example complete!")


if __name__ == '__main__':
    main()

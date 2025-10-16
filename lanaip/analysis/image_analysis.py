"""
Image Analysis Module

This module provides tools for analyzing reconstructed PET/SPECT/CT images.
"""

import numpy as np
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """
    Class for basic image analysis operations.
    """
    
    def __init__(self):
        """Initialize image analyzer."""
        logger.info("Initialized ImageAnalyzer")
    
    def calculate_roi_statistics(
        self,
        image: np.ndarray,
        roi_mask: np.ndarray
    ) -> dict:
        """
        Calculate statistics within a region of interest.
        
        Args:
            image: Input image array
            roi_mask: Boolean mask defining ROI
        
        Returns:
            Dictionary with statistics (mean, std, max, min, sum)
        """
        roi_values = image[roi_mask]
        
        stats = {
            'mean': np.mean(roi_values),
            'std': np.std(roi_values),
            'max': np.max(roi_values),
            'min': np.min(roi_values),
            'sum': np.sum(roi_values),
            'num_voxels': len(roi_values)
        }
        
        return stats
    
    def calculate_contrast(
        self,
        image: np.ndarray,
        hot_roi: np.ndarray,
        background_roi: np.ndarray
    ) -> float:
        """
        Calculate contrast between hot region and background.
        
        Args:
            image: Input image array
            hot_roi: Boolean mask for hot region
            background_roi: Boolean mask for background
        
        Returns:
            Contrast value
        """
        hot_mean = np.mean(image[hot_roi])
        bg_mean = np.mean(image[background_roi])
        
        if bg_mean == 0:
            return float('inf')
        
        contrast = (hot_mean - bg_mean) / bg_mean
        return contrast

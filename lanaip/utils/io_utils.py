"""
I/O Utilities Module

This module provides utility functions for reading and writing 
various medical imaging file formats.
"""

import numpy as np
import logging
from pathlib import Path
from typing import Union, Tuple, Optional

logger = logging.getLogger(__name__)


def load_image(filepath: Union[str, Path]) -> Tuple[np.ndarray, dict]:
    """
    Load medical image from file.
    
    Args:
        filepath: Path to image file
    
    Returns:
        Tuple of (image array, metadata dict)
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Placeholder for actual format readers
    logger.warning("Generic image loader. Implement specific format readers.")
    
    # For .npy files
    if filepath.suffix == '.npy':
        image = np.load(filepath)
        metadata = {'filename': str(filepath)}
        return image, metadata
    
    raise NotImplementedError(f"File format {filepath.suffix} not yet supported")


def save_image(
    image: np.ndarray,
    filepath: Union[str, Path],
    metadata: Optional[dict] = None
):
    """
    Save medical image to file.
    
    Args:
        image: Image array
        filepath: Output file path
        metadata: Optional metadata dictionary
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # For .npy files
    if filepath.suffix == '.npy':
        np.save(filepath, image)
        logger.info(f"Image saved to {filepath}")
        return
    
    raise NotImplementedError(f"File format {filepath.suffix} not yet supported")

"""
LANAIP - Image Reconstruction and Analysis Tools

This package provides tools for PET/SPECT/CT image reconstruction and analysis
for the LANAIP laboratory's Bruker Albira Si scanner.

Modules:
    reconstruction: List mode to sinogram conversion and image reconstruction
    analysis: Image analysis and processing tools
    utils: Utility functions for I/O and data handling
"""

__version__ = "0.1.0"
__author__ = "LANAIP Laboratory"
__description__ = "Image reconstruction and analysis tools for Bruker Albira Si scanner"

from . import reconstruction
from . import analysis
from . import utils

__all__ = ['reconstruction', 'analysis', 'utils']

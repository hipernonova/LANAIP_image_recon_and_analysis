# LANAIP Documentation

## Overview

This directory contains documentation for the LANAIP Image Reconstruction and Analysis package.

## Contents

- **Installation Guide**: How to install and set up the package
- **User Guide**: Basic usage and examples
- **API Reference**: Detailed API documentation
- **Developer Guide**: Information for contributors

## Quick Links

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from lanaip.reconstruction import convert_lm_to_sinogram

# Convert list mode to sinogram
sinogram = convert_lm_to_sinogram('input.lm', 'output.npy')
```

## Getting Started

1. See the [examples](../examples/) directory for usage examples
2. Run the reconstruction example: `python examples/reconstruction_example.py`
3. Run the analysis example: `python examples/analysis_example.py`

## Modules

### Reconstruction Module

- **lm2sinogram.py**: List mode to sinogram conversion
- **stir_wrapper.py**: STIR reconstruction interface

### Analysis Module

- **image_analysis.py**: Image analysis tools

### Utils Module

- **io_utils.py**: I/O utilities for various file formats

## Support

For issues and questions, please use the GitHub issue tracker.

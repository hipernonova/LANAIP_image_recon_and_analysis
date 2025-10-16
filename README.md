# LANAIP Image Reconstruction and Analysis

Repository with image reconstruction and analysis tools for the LANAIP laboratory which has a small animal PET/SPECT/CT scanner Bruker Albira Si.

## Overview

This package provides tools for:
- **List Mode to Sinogram Conversion**: Convert raw list mode data to sinogram format
- **Image Reconstruction**: Interface to STIR (Software for Tomographic Image Reconstruction)
- **Image Analysis**: Tools for analyzing reconstructed PET/SPECT/CT images

## Features

- ✅ List mode data processing for Bruker Albira Si scanner
- ✅ Sinogram generation with configurable parameters
- ✅ Time and energy windowing
- ✅ ROI analysis and statistics
- ✅ Python and C code support
- 🔄 STIR integration (in development)

## Installation

### Prerequisites

- Python 3.7 or higher
- NumPy, SciPy, Matplotlib

### Install from source

```bash
git clone https://github.com/mabelzunce/LANAIP_image_recon_and_analysis.git
cd LANAIP_image_recon_and_analysis
pip install -e .
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### List Mode to Sinogram Conversion

```python
from lanaip.reconstruction import convert_lm_to_sinogram

# Simple conversion
sinogram = convert_lm_to_sinogram('data.lm', 'output.npy')

# With time and energy windows
sinogram = convert_lm_to_sinogram(
    'data.lm',
    'output.npy',
    time_window=(10, 100),      # 10-100 seconds
    energy_window=(450, 570)    # 450-570 keV
)
```

### Advanced Usage

```python
from lanaip.reconstruction import ListModeToSinogram

# Create converter with custom parameters
converter = ListModeToSinogram(
    num_rings=4,
    num_detectors_per_ring=160,
    num_bins_s=128,
    num_bins_phi=128,
    max_ring_diff=3
)

# Get configuration info
info = converter.get_sinogram_info()
print(info)

# Convert with filters
sinogram = converter.convert(
    lm_data='data.lm',
    output_file='sinogram.npy',
    time_window=(0, 60),
    energy_window=(450, 570)
)
```

### Image Analysis

```python
from lanaip.analysis.image_analysis import ImageAnalyzer
import numpy as np

analyzer = ImageAnalyzer()

# Calculate ROI statistics
stats = analyzer.calculate_roi_statistics(image, roi_mask)
print(f"Mean: {stats['mean']:.2f}")
print(f"Std: {stats['std']:.2f}")

# Calculate contrast
contrast = analyzer.calculate_contrast(image, hot_roi, background_roi)
print(f"Contrast: {contrast:.2f}")
```

## Directory Structure

```
LANAIP_image_recon_and_analysis/
├── README.md                 # This file
├── LICENSE                   # License information
├── .gitignore               # Git ignore rules
├── setup.py                 # Package installation script
├── requirements.txt         # Python dependencies
├── src/                     # Source code directory
│   ├── lanaip/              # Main package
│   │   ├── __init__.py
│   │   ├── reconstruction/  # Reconstruction tools
│   │   │   ├── __init__.py
│   │   │   ├── lm2sinogram.py  # List mode to sinogram converter
│   │   │   └── stir_wrapper.py # STIR interface
│   │   ├── analysis/       # Analysis tools
│   │   │   ├── __init__.py
│   │   │   └── image_analysis.py
│   │   └── utils/          # Utility functions
│   │       ├── __init__.py
│   │       └── io_utils.py
│   └── c_extensions/       # C code extensions
│       └── README.md
├── examples/               # Example scripts
│   ├── reconstruction_example.py
│   └── analysis_example.py
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_lm2sinogram.py
└── docs/                   # Documentation
    └── README.md
```

## Examples

Run the example scripts to see the package in action:

```bash
# Reconstruction example
python examples/reconstruction_example.py

# Analysis example
python examples/analysis_example.py
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Scanner Specifications

**Bruker Albira Si Scanner:**
- Modalities: PET, SPECT, CT
- PET Configuration:
  - Number of rings: 4
  - Detectors per ring: 160
  - Energy resolution: ~18% at 511 keV
  - Spatial resolution: ~1.5 mm

## Development

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Roadmap

- [ ] Complete STIR integration
- [ ] Add support for Bruker native file formats
- [ ] Implement attenuation correction
- [ ] Add scatter correction
- [ ] Create GUI for interactive analysis
- [ ] Add C extensions for performance

## Dependencies

- **numpy**: Array operations and numerical computing
- **scipy**: Scientific computing utilities
- **matplotlib**: Visualization (optional)

## License

[Add license information here]

## Contact

LANAIP Laboratory
[Add contact information]

## Citation

If you use this software in your research, please cite:

```
[Add citation information]
```

## Acknowledgments

This project uses:
- STIR: Software for Tomographic Image Reconstruction
- NumPy and SciPy: Scientific computing libraries

## References

1. Bruker Albira Si Scanner Documentation
2. STIR Documentation: http://stir.sourceforge.net/
3. PET/SPECT Image Reconstruction Literature

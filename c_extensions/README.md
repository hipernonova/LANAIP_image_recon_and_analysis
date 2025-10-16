# C Extensions for LANAIP

This directory is intended for C code extensions that can accelerate performance-critical operations.

## Purpose

C extensions can be used for:
- Fast list mode event processing
- Sinogram binning acceleration
- Detector geometry calculations
- Image reconstruction kernels

## Building C Extensions

Future implementations will use tools like:
- Cython for Python-C integration
- pybind11 for modern C++ bindings
- ctypes for simple C library wrapping

## Planned Extensions

1. **fast_histogram.c**: Accelerated histogramming for list mode data
2. **geometry.c**: Scanner geometry calculations
3. **corrections.c**: Attenuation and scatter correction routines

## Example Structure

```
c_extensions/
├── README.md
├── src/
│   ├── fast_histogram.c
│   └── geometry.c
├── include/
│   └── lanaip_c.h
└── setup_c.py
```

## Notes

- C extensions are optional
- Pure Python implementations are provided as fallback
- C code should be well-documented and tested

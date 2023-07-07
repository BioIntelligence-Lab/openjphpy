# openjphpy

**Note:** This repository is currently work in progress. Please contact us for more details [here](mailto:pkulkarni@som.umaryland.edu,vparekh@som.umaryland.edu).

## What is openjphpy?

A Python wrapper for [OpenJPH](https://github.com/aous72/OpenJPH) to enable encoding and/or decoding High-Throughput JPEG 2000 (HTJ2K) images.

In short, OpenJPH is an open-source implementation of the HTJ2K codec (JPEG2000 Part 15, ISO/IEC 15444-15, and ITU-T T.814), supporting features defined in JPEG 2000 Part 1. The code is written in C++ with color and wavelet transform steps taking advantage of SIMD instructions on Intel platforms. Unfortunately, this restricts encoding and/or decoding on image data directly from other commonly used programming languages. For example, another project [openjphjs](https://github.com/chafey/openjphjs), developed by [Chris Hafey](https://github.com/chafey), brings OpenJPH's capabilities to Javascript. Similarly, we aim to bring these capabilities to Python with direct support for HTJ2K encoding/decoding using **openjphpy**.

We use openjphpy in our implementation of the [Medical Image Streaming Toolkit (MIST)](https://github.com/UM2ii/MIST), an open-source toolkit to operationalize and democratize progressive resolution for large-scale medical imaging data infrastructures to accelerate data transmission and AI modelling. You can read our paper on MIST [here](https://arxiv.org/abs/2307.00438).

### Resources

For more resources regarding HTJ2K, please refer to:
- [HTJ2K White Paper](http://ds.jpeg.org/whitepapers/jpeg-htj2k-whitepaper.pdf)
- [High throughput JPEG 2000 (HTJ2K): Algorithm, performance and potential](https://htj2k.com/wp-content/uploads/white-paper.pdf)
- [High throughput block coding in the HTJ2K compression standard](http://kakadusoftware.com/wp-content/uploads/icip2019.pdf) 

### Citation

If you use openjphpy in your publication, please cite it using:

```text
@software{openjphpy,
author = {Kulkarni, Pranav},
title = {{openjphpy}},
month = {July},
year = {2023},
url = {https://github.com/UM2ii/openjphpy}
}
```

## Getting Started

Currently, openjphpy can only be installed manually from source.

```text
git clone --recurse-submodules https://github.com/UM2ii/openjphpy
pip install -e openjphpy/
```

**Note:** openjphpy is only supported on Linux based environments with support for other environments coming in the future.

### Example Notebook

We have provides an example notebook in this repository, along with 10 test images, to experiment with. You can find the example notebook [here](openjphpy/notebooks/example.ipynb).

## Future Work

In the future, we intend to extend support to non-Linux environments. Similarly, we intend to employ a similar approach used by [openjphjs](https://github.com/chafey/openjphjs) to integrate native C++ code directly into Python. While our currently implementation supports the entire feature set of OpenJPH, it is not the most efficient implementation. We invite collaborators in the open-source community to help integrate with OpenJPH's native C++ code with direct encode/decode capabilities in Python.

## Documentation

Complete documentation for openjphpy is available [here](./docs/openjphpy.md).

## Contact

If you have any questions about openjphpy, please contact us [here](mailto:pkulkarni@som.umaryland.edu,vparekh@som.umaryland.edu).
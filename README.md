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

If you use openjphpy in your publication, please cite the following:

- GitHub
```text
@software{openjphpy,
author = {Kulkarni, Pranav},
title = {{openjphpy}},
month = {July},
year = {2023},
url = {https://github.com/UM2ii/openjphpy}
}
```
- Publication
```text
@article{kulkarni2023one,
  title={One Copy Is All You Need: Resource-Efficient Streaming of Medical Imaging Data at Scale},
  author={Kulkarni, Pranav and Kanhere, Adway and Siegel, Eliot and Yi, Paul H and Parekh, Vishwa S},
  journal={arXiv preprint arXiv:2307.00438},
  year={2023}
}
```

## Getting Started

Currently, openjphpy can only be installed manually from source.

```text
git clone --recurse-submodules https://github.com/UM2ii/openjphpy
pip install -e openjphpy/
```

Documentation for openjphpy is available [here](./docs/openjphpy.md).

**Note:** openjphpy is only supported on Linux based environments with support for other environments coming in the future.

### Example Notebook

We have provided an example notebook in this repository, along with 10 test images, to experiment with. You can find the example notebook [here](openjphpy/notebooks/example.ipynb).

We also provide [15 sample medical images](./data/) across X-ray, MRI, and CT modalities (5 images per modality), with data sourced from the [NIH Chest X-Ray 14](https://arxiv.org/abs/1705.02315) and [Medical Segmentation Decathlon (MSD)](http://medicaldecathlon.com/) datasets. For portability, all data is stored as `npy` files. 

**Note:** CT data is stored as uint16 and not in Hounsfield units.

## Limitations

Currently, openjphpy does not support encoding signed data and can only encode imaging data with types 8-bit and 16-bit unsigned integers (uint8 and uint16). If pixel values fall outside the range [0, 65,535], an error may be raised (strict mode) or values will be clipped (non-strict mode). Precision is automatically chosen based on image data's dynamic range.

## Future Work

In the future, we intend to extend support to non-Linux environments. Similarly, we intend to employ a similar approach used by [openjphjs](https://github.com/chafey/openjphjs) to integrate native C++ code directly into Python. While our current implementation supports the entire feature set of OpenJPH, it is not computationally optimized. We invite collaborators in the open-source community to help integrate with OpenJPH's native C++ code with direct encode/decode capabilities in Python.

## Contact

If you have any questions about openjphpy, please contact us [here](mailto:pkulkarni@som.umaryland.edu,vparekh@som.umaryland.edu).

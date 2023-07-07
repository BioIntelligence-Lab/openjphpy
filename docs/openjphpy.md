## `encode`

Encodes array containing image data into HTJ2K bytestream using OpenJPH.

### Arguments:
- filename : str 
  - Output file name (either jph or j2c for backwards compatibility with JPEG 2000)
- img : np.ndarray 
  - An array containing image data. Currently only 8-bit and 16-bit unsigned integers (uint8 and uint16) are supported. If pixel values fall outside the range [0, 65535], an error may be raised (strict mode) or values will be clipped (non-strict mode). Precision is automatically chosen based on image data's dynamic range.
- strict : bool, optional 
  - Enables strict mode for encoder. Strict mode stops encoding if paths do not exist or pixel values are being clipped. Defaults to False.
- **kwargs
  - Modifies encoder parameters. See documentation for [`backend.ojph_compress`](./backend.md#ojph_compress).

### Returns:
- float : 
  - Time taken to encode image data.

## `decode`

Decodes HTJ2K bytestream into array containing image data using OpenJPH.

### Arguments:
- filename : str 
  - Input file name (either jph or j2c)
- **kwargs :
  - Modifies decoder parameters. See documentation for [`backend.ojph_expand`](./backend.md#ojph_expand).

### Returns:
- np.ndarray :
  - An array containing image data.
- float : 
  - Time taken to decode image data.

## `__PRECISION_WARNING`

Flag to check if precision warning has been raised in non-strict encoding.
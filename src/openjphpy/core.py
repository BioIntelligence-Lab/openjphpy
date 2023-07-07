from .backend import ojph_expand, ojph_compress

import numpy as np
import cv2
import os
import warnings
import tempfile

__PRECISION_WARNING = False
"""
Flag to check if precision warning has been raised in non-strict encoding.
"""

def encode(
  filename : str,
  img : np.ndarray, 
  strict : bool = False,
  **kwargs,
) -> float:
  """
  Encodes array containing image data into HTJ2K bytestream using OpenJPH.

  ## Arguments:
  filename : str 
    Output file name (either jph or j2c for backwards compatibility with JPEG 2000)
  img : np.ndarray 
    An array containing image data. Currently only 8-bit and 16-bit unsigned integers (uint8 and uint16) are supported. If pixel values fall outside the range [0, 65535], an error may be raised (strict mode) or values will be clipped (non-strict mode). Precision is automatically chosen based on image data's dynamic range.
  strict : bool, optional 
    Enables strict mode for encoder. Strict mode stops encoding if paths do not exist or pixel values are being clipped. Defaults to False.
  **kwargs
    Modifies encoder parameters. See documentation for :func:`backend.ojph_compress`.

  ## Returns:
  float : 
    Time taken to encode image data.
  """
  global __PRECISION_WARNING
  # Create parent directory for output file in non-strict mode
  if not strict:
    dirname = os.path.dirname(filename)
    if dirname:
      os.makedirs(dirname, exist_ok=True)
  # Check precision of input image
  # Due to limitations in this implementation, only uint8 + uint16 are supported
  if img.dtype != np.uint8 or img.dtype != np.uint16:
    min_val, max_val = np.min(img), np.max(img)
    # Check if input image exceeds precision supported by uint16
    if min_val < 0 or max_val > 65535:
      # Raise error in strict mode. Otherwise, warn once and clip image
      if strict:
        raise ValueError('Precision Error! Currently only 8-bit and 16-bit unsigned integers (uint8 and uint16) are supported')
      else:
        if not __PRECISION_WARNING:
          warnings.warn('Precision Warning! Currently only 8-bit and 16-bit unsigned integers (uint8 and uint16) are supported. Pixel values will be clipped in non-strict mode')
          __PRECISION_WARNING = True
    # Transform input image into correct dtype
    # This automatically clips pixel values in non-strict mode
    if max_val > 255:
      img = img.astype(np.uint16)
    else:
      img = img.astype(np.uint8)
  # TODO: Add support for 3-channel ppm files
  # Using temporary files to automatically clear intermediate pgm files
  with tempfile.NamedTemporaryFile(suffix='.pgm', prefix='encode_') as temp:
    # Write intermediate pgm file
    cv2.imwrite(temp.name, img)
    # Encode pgm using backend
    encode_time = ojph_compress(temp.name, filename, **kwargs)
    temp.flush()
  return encode_time

def decode(
  filename : str,
  **kwargs
) -> tuple[np.ndarray, float]:
  """
  Decodes HTJ2K bytestream into array containing image data using OpenJPH.

  ## Arguments:
  filename : str 
    Input file name (either jph or j2c)
  **kwargs :
    Modifies decoder parameters. See documentation for :func:`backend.ojph_expand`.

  ## Returns:
  np.ndarray :
    An array containing image data.
  float : 
    Time taken to decode image data.
  """
  # Using temporary files to automatically clear intermediate pgm files
  with tempfile.NamedTemporaryFile(suffix='.pgm', prefix='encode_') as temp:
    # Decode to pgm using backend
    decode_time = ojph_expand(filename, temp.name, **kwargs)
    # Read intermediate pgm file
    img = cv2.imread(temp.name, cv2.IMREAD_UNCHANGED)
    temp.flush()
  return img, decode_time
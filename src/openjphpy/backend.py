import subprocess
import numpy as np
from enum import Enum
from typing import Union

class ProgressionOrder(Enum):
  """
  Collection of progression orders supported by OpenJPH.
  
  According to the JPEG 2000 codec, progression order lets you specify the order in which packets will appear in a given file and may have a significant impact on the time and memory usage required to encode and/or decode the image. Default is RPCL.
  """
  LRCP = 'LRCP'
  RLCP = 'RLCP'
  RPCL = 'RPCL'
  PCRL = 'PCRL'
  CPRL = 'CPRL'
  
class Tileparts(Enum):
  """
  Collection of tilepart grouping supported by OpenJPH.
  
  According to the JPEG 2000 codec, tileparts define the group of packets that are written together. Tile parts can be grouped by resolution (R), layer, or component (C), depending on which progression order you use. By default, no grouping option is selected and the file is written sequentially.
  """
  R = 'R'
  C = 'C'
  RC = 'RC'
  
def __format_args(
  x : Union[np.ndarray, tuple, list],
) -> str:
  """
  Formats comma-separated sequence of values for OpenJPH interpretation.

  ## Arguments
  x (array-like): 
    Sequence of values paired values {x,y},{x,y},...,{x,y}

  ## Returns
  str : 
    Formatted comma-separated sequence of values
  """
  x = np.array(x, dtype=int)
  if x.ndim == 1:
    x = np.expand_dims(x, axis=0)
  formatted_str = []
  for x_i in x:
    if len(x_i) != 2:
      raise ValueError('Invalid value! Input must be a sequence of two comma-separated values, enclosed within curly braces. See usage.')
    formatted_str += [f'{{{x_i[0]},{x_i[1]}}}']
  return ','.join(formatted_str)

def ojph_compress(
  input_path : str,
  output_path : str,
  num_decomps : int = 5,
  qstep : float = 0.0039,
  reversible : bool = False,
  color_trans : bool = True,
  prog_order : ProgressionOrder = ProgressionOrder.RPCL,
  block_size : Union[np.ndarray, tuple[int, int], list[int]] = (64,64),
  precints : Union[np.ndarray, list[tuple[int,int]]] = None,
  tile_offset : Union[np.ndarray, tuple[int, int], list[int]] = None,
  tile_size : Union[np.ndarray, tuple[int, int], list[int]] = None,
  image_offset : Union[np.ndarray, tuple[int, int], list[int]] = None,
  tileparts : Tileparts = None,
  tlm_marker : bool = False,
) -> float:
  """
  Python wrapper for OpenJPH's :func:`ojph_compress`.

  ## Arguments
  input_path : str 
    Input file name (either pgm or ppm)
  output_path : str
    Output file name
  num_decomps : int, optional
    Number of decompositions. Defaults to 5.
  qstep : float, optional
    Quantization step size for lossy compression; quantization steps size for all subbands are derived from this value. Defaults to 0.0039 for 8-bit images.
  reversible : bool, optional
    This should be false to perform lossy compression using the 9/7 wavelet transform; or true to perform reversible compression, where the 5/3 wavelet is employed with lossless compression. Defaults to False.
  color_trans : bool, optional
    This option employs a color transform, to transform RGB color images into the YUV domain. This option should not be used with YUV images, because they have already been transformed. If there are three color components that are downsampled by the same amount then the color transform can be true or false. This option is also available when there are more than three colour components, where it is applied to the first three colour components. It has already been applied to convert the original RGB or whatever the original format to YUV. Defaults to True.
  prog_order : backend.ProgressionOrder, optional
    Progression order and can be one of: LRCP, RLCP, RPCL, PCRL, CPRL. Defaults to RPCL. See :func:`ProgressionOrder` for more details.
  block_size : array-like, optional
    {x,y} where x and y are the height and width of a codeblock. Defaults to (64,64).
  precints : array-like, optional
    {x,y},{x,y},...,{x,y} where {x,y} is the precinct size starting from the coarest resolution; the last precinct is repeated for all finer resolutions.
  tile_offset : array-like, optional 
    {x,y} tile offset.
  tile_size : array-like, optional
    {x,y} tile width and height..
  image_offset : array-like, optional
    {x,y} image offset from origin.
  tileparts : backend.Tileparts, optional
    Employs tilepart divisions at each resolution, indicated by the letter R, and/or component, indicated by the letter C. By default, no grouping option is selected and the file is written sequentially.
  tlm_marker : bool, optional
    Inserts a TLM markers in bytestream. Defaults to False.

  ## Returns
  float : 
    Time taken to encode image data.
  """  
  # Construct arguments using default values
  args = [
    'ojph_compress',
    '-i', f'{input_path}',
    '-o', f'{output_path}',
    '-num_decomps', f'{num_decomps}'.lower(),
    '-prog_order', prog_order.value,
    '-block_size', __format_args(block_size),
    '-tlm_marker', f'{tlm_marker}'.lower(),
  ]
  # Only apply color transform from RGB to YUV for 3-channel ppm images
  if '.ppm' in input_path:
    args += [
      '-colour_trans', f'{color_trans}'.lower(),
    ]
  # Only include quantization step if lossless/non-reversible
  if reversible == True:
    args += [
      '-reversible', 'true',
    ]
  elif reversible == False:
    args += [
      '-qstep', f'{qstep}',
      '-reversible', 'false',
    ]
  else:
    raise ValueError('Invalid value! `reversible` must be a boolean')
  # Add optional arguments as needed
  if precints:
    args += ['-precints', __format_args(precints)]
  if tile_offset:
    args += ['-tile_offset', __format_args(tile_offset)]  
  if tile_size:
    args += ['-tile_size', __format_args(tile_size)] 
  if image_offset:
    args += ['-image_offset', __format_args(image_offset)] 
  if tileparts:
    args += ['-tileparts', tileparts.value]
  # Execute `ojph_compress` in background
  output = subprocess.run(
    args,
    capture_output = True
  )
  # If successful, return encode time. Otherwise raise error
  if output.stdout:
    return float(output.stdout.decode('utf-8').replace('Elapsed time = ', ''))
  else:
    raise ValueError(output.stderr.decode('utf-8'))

def ojph_expand(
  input_path : str,
  output_path : str,
  skip_res : Union[int, np.ndarray, tuple[int,int], list[int]] = None,
  resilient : bool = False,
) -> float:
  """
  Python wrapper for OpenJPH's :func:`ojph_expand`.

  ## Arguments
  input_path : str
    input file name
  output_path : str
    output file name (either pgm or ppm)
  skip_res : array-like, optional
    x,y a comma-separated list of two elements containing the number of resolutions to skip. You can specify 1 or 2 parameters; the first specifies the number of resolution for which data reading is skipped. The second is the number of skipped resolution for reconstruction, which is either equal to the first or smaller. If the second is not specified, it is made to equal to the first. Defaults to None.
  resilient : bool, optional
    Makes decoder to be more tolerant of errors in the codestream. Defaults to False.

  ## Returns
  float : 
    Time taken to decode image data.
  """  
  # Construct arguments using default values
  args = [
    'ojph_expand',
    '-i', f'{input_path}',
    '-o', f'{output_path}',
    '-resilient', f'{resilient}'.lower(),
  ]
  # Add optional argument as needed
  if skip_res:
    # `skip_res` can be list of two numbrs or just a single number
    if isinstance(skip_res, (list, tuple, np.ndarray)):
      # Check if `skip_res` args are valid before append
      if len(skip_res) != 2:
        raise ValueError('Invalid value! `skip_res` must be x,y a comma-separated list of two elements containign the number of resolutions to skip')
      args += [
        '-skip_res', f'{skip_res[0]},{skip_res[1]}'
      ]
    else:
      args += [
        '-skip_res', f'{skip_res}'
      ]
  # Execute `ojph_expand` in background
  output = subprocess.run(
    args, 
    capture_output=True
  )
  # If successful, return decode time. Otherwise raise error
  if output.stdout:
    return float(output.stdout.decode('utf-8').replace('Elapsed time = ', ''))
  else:
    raise ValueError(output.stderr.decode('utf-8'))
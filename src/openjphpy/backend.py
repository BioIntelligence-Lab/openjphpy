import subprocess
import numpy as np
from enum import Enum
from typing import Union

def __format_args(x : Union[np.ndarray, tuple, list]):
  x = np.array(x, dtype=int)
  if x.ndim == 1:
    x = np.expand_dims(x, axis=0)
  formatted_str = []
  for x_i in x:
    if len(x_i) != 2:
      raise ValueError('Invalid value! Input must be a sequence of two comma-separated values, enclosed within curly braces. See usage.')
    formatted_str += [f'{{{x_i[0]},{x_i[1]}}}']
  return ','.join(formatted_str)

class ProgressionOrder(Enum):
  LRCP = 0
  RLCP = 1
  RPCL = 2
  PCRL = 3
  CPRL = 4
  
class Tileparts(Enum):
  R = 0
  C = 1
  RC = 2

OJPH_COMPRESS_USAGE = """
The following arguments are necessary:
 -i input file name (either pgm, ppm, or raw(yuv))
 -o output file name

The following option has a default value (optional):
 -num_decomps  (5) number of decompositions
 -qstep        (0.00001...0.5) quantization step size for lossy
               compression; quantization steps size for all subbands are
               derived from this value. {The default value for 8bit
               images is 0.0039}
 -reversible   (false) for irreversible; this should be false to perform
               lossy compression using the 9/7 wavelet transform;
               or true to perform reversible compression, where
               the 5/3 wavelet is employed with lossless compression.
 -colour_trans (true) this option employs a color transform, to
               transform RGB color images into the YUV domain.
               This option should not be used with YUV images, because
               they have already been transformed.
               If there are three color components that are
               downsampled by the same amount then the color transform
               can be true or false. This option is also available
               when there are more than three colour components,
               where it is applied to the first three colour
               components.
               it has already been applied to convert the original RGB
               or whatever the original format to YUV.
 -prog_order   (RPCL) is the progression order, and can be one of:
               LRCP, RLCP, RPCL, PCRL, CPRL
 -block_size   {x,y} (64,64) where x and y are the height and width of
               a codeblock. In unix-like environment, { and } must be
               proceeded by a \
 -precincts    {x,y},{x,y},...,{x,y} where {x,y} is the precinct size
               starting from the coarest resolution; the last precinct
               is repeated for all finer resolutions
 -tile_offset  {x,y} tile offset.
 -tile_size    {x,y} tile width and height.
 -image_offset {x,y} image offset from origin.
 -tileparts    (None) employ tilepart divisions at each resolution,
               indicated by the letter R, and/or component, indicated
               by the letter C. For both, use "-tileparts RC".
 -tlm_marker   (false) insert a TLM marker, either "true" or "false"
 -profile      (None) is the profile, the code will check if the
               selected options meet the profile.  Currently only
               BROADCAST and IMF are supported.  This automatically
               sets tlm_marker to true and tileparts to C.
"""

OJPH_EXPAND_USAGE = """
The following arguments are necessary:
 -i input file name
 -o output file name (either pgm, ppm, or raw(yuv))

The following arguments are options:
 -skip_res  x,y a comma-separated list of two elements containing the
            number of resolutions to skip. You can specify 1 or 2
            parameters; the first specifies the number of resolution
            for which data reading is skipped. The second is the
            number of skipped resolution for reconstruction, which is
            either equal to the first or smaller. If the second is not
            specified, it is made to equal to the first.
 -resilient true if you want the decoder to be more tolerant of errors
            in the codestream
"""

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
  tlm_marker : bool = False
):
  args = [
    'ojph_compress',
    '-i', f'{input_path}',
    '-o', f'{output_path}',
    '-num_decomps', f'{num_decomps}'.lower(),
    '-colour_trans', f'{color_trans}'.lower(),
    '-prog_order', f'{prog_order}'.upper(),
    '-block_size', __format_args(block_size),
    '-tlm_marker', f'{tlm_marker}'.lower(),
  ]
  
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
    raise ValueError('Invalid value for `reversible`! Usage: \n', OJPH_COMPRESS_USAGE)
  
  if precints:
    args += ['-precints', __format_args(precints)]
  if tile_offset:
    args += ['-tile_offset', __format_args(tile_offset)]  
  if tile_size:
    args += ['-tile_size', __format_args(tile_size)] 
  if image_offset:
    args += ['-image_offset', __format_args(image_offset)] 
  if tileparts:
    args += ['-tileparts', f'{tileparts}'.upper()]
    
  output = subprocess.run(
    args,
    capture_output = True
  )
  if output.stdout:
    return float(output.stdout.decode('utf-8').replace('Elapsed time = ', ''))
  else:
    raise ValueError(output.stderr.decode('utf-8'))

def ojph_expand(
  input_path : str,
  output_path : str,
  skip_res : Union[int, np.ndarray, tuple[int,int], list[int]] = None,
  resilient : bool = False
):
  args = [
    'ojph_expand',
    '-i', f'{input_path}',
    '-o', f'{output_path}',
    '-resilient', f'{resilient}'.lower(),
  ]
  
  if skip_res:
    if isinstance(skip_res, (list, tuple, np.ndarray)):
      if len(skip_res) != 2:
        raise ValueError('Invalid value for `skip_res`! Usage: \n', OJPH_EXPAND_USAGE)
      args += [
        '-skip_res', f'{skip_res[0]},{skip_res[1]}'
      ]
    else:
      args += [
        '-skip_res', f'{skip_res}'
      ]
  
  output = subprocess.run(
    args, 
    capture_output=True
  )
  if output.stdout:
    return float(output.stdout.decode('utf-8').replace('Elapsed time = ', ''))
  else:
    raise ValueError(output.stderr.decode('utf-8'))
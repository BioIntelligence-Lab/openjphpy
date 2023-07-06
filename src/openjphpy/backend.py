import subprocess
import numpy as np

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
  input_path,
  output_path,
  num_decomps = 5,
  qstep = 0.0039,
  reversible = False,
  color_trans = True,
  prog_order = 'RPCL',
  block_size = (64,64),
  precints = None,
  tile_offset = None,
  tile_size = None,
  tileparts = None,
  tlm_marker = False,
):
  # args = f'ojph_compress -i "{input_path}" -o "{output_path}" -reversible true -num_decomps {num_decomps} -tlm_marker true -tileparts R', 
  
  args = [
    'ojph_compress',
    '-i', f'{input_path}',
    '-o', f'{output_path}',
    '-num_decomps', f'{num_decomps}',
    '-color_trans', f'{color_trans}',
    '-prog_order', f'{prog_order}',
    '-block_size', f'{{{block_size[0]},{block_size[1]}}}',
    '-tlm_marker', f'{tlm_marker}',
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
    args += ['-precints', f'{precints}']
  if tile_offset:
    args += ['-tile_offset', f'{tile_offset}']  
  if tile_size:
    args += ['-tile_size', f'{tile_size}'] 
  if tileparts:
    args += ['-tileparts', f'{tileparts}']
    
  output = subprocess.run(
    args,
    # shell = True, 
    capture_output = True
  )
  if output.stdout:
    return float(output.stdout.decode('utf-8').replace('Elapsed time = ', ''))
  else:
    raise ValueError(output.stderr)

def ojph_expand(
  input_path,
  output_path,
  skip_res = None,
  resilient = False
):
  # args = f'ojph_expand -i "{input_path}" -o "{output_path}" -skip_res {skip_res}'
  
  args = [
    'ojph_expand',
    '-i', f'{input_path}',
    '-o', f'{output_path}',
    '-resilient', f'{resilient}',
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
    # shell=True,
    capture_output=True
  )
  if output.stdout:
    return float(output.stdout.decode('utf-8').replace('Elapsed time = ', ''))
  else:
    raise ValueError(output.stderr)
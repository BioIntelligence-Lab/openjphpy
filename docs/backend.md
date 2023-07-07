## `ProgressionOrder`

Collection of progression orders supported by OpenJPH.
  
According to the JPEG 2000 codec, progression order lets you specify the order in which packets will appear in a given file and may have a significant impact on the time and memory usage required to encode and/or decode the image. Default is RPCL.

## `Tileparts`

Collection of tilepart grouping supported by OpenJPH.
  
According to the JPEG 2000 codec, tileparts define the group of packets that are written together. Tile parts can be grouped by resolution (R), layer, or component (C), depending on which progression order you use. By default, no grouping option is selected and the file is written sequentially.

## `__format_args`

Formats comma-separated sequence of values for OpenJPH interpretation.

### Arguments
- x (array-like): 
  - Sequence of values paired values {x,y},{x,y},...,{x,y}

### Returns
- str : 
  - Formatted comma-separated sequence of values

## `ojph_compress`

Python wrapper for OpenJPH's `ojph_compress`.

### Arguments
- input_path : str 
  - Input file name (either pgm or ppm)
- output_path : str
  - Output file name
- num_decomps : int, optional
  - Number of decompositions. Defaults to 5.
- qstep : float, optional
  - Quantization step size for lossy compression; quantization steps size for all subbands are derived from this value. Defaults to 0.0039 for 8-bit images.
- reversible : bool, optional
  - This should be false to perform lossy compression using the 9/7 wavelet transform; or true to perform reversible compression, where the 5/3 wavelet is employed with lossless compression. Defaults to False. Defaults to False.
- color_trans : bool, optional
  - This option employs a color transform, to transform RGB color images into the YUV domain. This option should not be used with YUV images, because they have already been transformed. If there are three color components that are downsampled by the same amount then the color transform can be true or false. This option is also available when there are more than three colour components, where it is applied to the first three colour components. It has already been applied to convert the original RGB or whatever the original format to YUV. Defaults to True.
- prog_order : backend.ProgressionOrder, optional
  - Progression order and can be one of: LRCP, RLCP, RPCL, PCRL, CPRL. Defaults to RPCL. See [`ProgressionOrder`](./backend.md#progressionorder) for more details.
- block_size : array-like, optional
  - {x,y} where x and y are the height and width of a codeblock. Defaults to (64,64).
- precints : array-like, optional
  - {x,y},{x,y},...,{x,y} where {x,y} is the precinct size starting from the coarest resolution; the last precinct is repeated for all finer resolutions.
- tile_offset : array-like, optional 
  - {x,y} tile offset.
- tile_size : array-like, optional
  - {x,y} tile width and height..
- image_offset : array-like, optional
  - {x,y} image offset from origin.
- tileparts : backend.Tileparts, optional
  - Employs tilepart divisions at each resolution, indicated by the letter R, and/or component, indicated by the letter C. By default, no grouping option is selected and the file is written sequentially.
- tlm_marker : bool, optional
  - Inserts a TLM markers in bytestream. Defaults to False.

### Returns
- float : 
  - Time taken to encode image data.

## `ojph_expand`

Python wrapper for OpenJPH's `ojph_expand`.

### Arguments
- input_path : str
  - input file name
- output_path : str
  - output file name (either pgm or ppm)
- skip_res : array-like, optional
  - x,y a comma-separated list of two elements containing the number of resolutions to skip. You can specify 1 or 2 parameters; the first specifies the number of resolution for which data reading is skipped. The second is the number of skipped resolution for reconstruction, which is either equal to the first or smaller. If the second is not specified, it is made to equal to the first. Defaults to None.
- resilient : bool, optional
  - Makes decoder to be more tolerant of errors in the codestream. Defaults to False.

### Returns
- float : 
  - Time taken to decode image data.
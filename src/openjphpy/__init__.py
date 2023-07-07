from .core import encode, decode

import os

def import_ojph():
  """
  Includes compiled OpenJPH files in Python $PATH variable on import
  """
  if 'openjph/bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openjph/bin')
    
import_ojph()
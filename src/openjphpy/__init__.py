from .backend import ojph_compress, ojph_expand
from .core import encode, decode

import sys
import os

def import_ojph():
  if 'openjph/bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openjph/bin')
    
import_ojph()
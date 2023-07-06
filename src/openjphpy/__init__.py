from .backend import ojph_compress, ojph_expand
from .core import encode, decode

import sys
import os

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openjph/bin'))

os.environ["PATH"] += os.pathsep + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openjph/bin')
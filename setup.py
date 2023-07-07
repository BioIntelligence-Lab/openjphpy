from setuptools import setup, find_packages
import subprocess
import sys

src_path = 'src/openjphpy/openjph'
build_path = 'src/openjphpy/openjph/build'

def compile_linux():
  """
  Compile OpenJPH source code in linux environment.

  Raises:
      SystemError: Error is raised if compilation fails
  """
  response = subprocess.run(
    [
      'cmake', 
      '-DCMAKE_BUILD_TYPE=Release', 
      '-S', src_path, 
      '-B', build_path,
      ';',
      'make', 
      '-C', build_path
    ],
    capture_output = True
  )
  if response.stderr:
    raise SystemError(response.stderr)

def compile_openjph():
  """
  Compile OpenJPH source code on install.
  """
  if 'linux' in sys.platform:
    compile_linux()
  else:
    raise NotImplementedError('Currently only linux support is implemented')

setup(
    name = 'openjphpy',
    version = '0.1.0',    
    description = 'A Python wrapper around OpenJPH for encoding and decoding High-Throughput JPEG 2000 (HTJ2K) images.',
    url = 'https://github.com/UM2ii/openjphpy',
    author = 'Pranav Kulkarni',
    author_email = 'pkulkarni@som.umaryland.edu',
    license = 'BSD',
    packages = find_packages(),
    package_dir = {'': 'src'},
    install_requires = [
      'opencv-python',
      'numpy',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',     
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires = ">=3.7",
    test_suite = 'tests',
)
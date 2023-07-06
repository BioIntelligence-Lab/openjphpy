from setuptools import setup, find_packages
import subprocess

src_path = 'src/openjph'
build_path = 'src/openjph/build'

cmake_linux = ['cmake', '-DCMAKE_BUILD_TYPE=Release', '-S', src_path, '-B', build_path]
make_linux = ['make', '-C', build_path]

def build_linux():
  subprocess.run(cmake_linux, stderr = subprocess.STDOUT)
  subprocess.run(make_linux, stderr = subprocess.STDOUT)

setup(
    name = 'openjphpy',
    version = '0.0.1',    
    description = 'A Python wrapper around OpenJPH for encoding and decoding High-Throughput JPEG 2000 (HTJ2K) images.',
    url = 'https://github.com/UM2ii/openjphpy',
    author = 'Pranav Kulkarni',
    author_email = 'pkulkarni@som.umaryland.edu',
    license = 'BSD',
    packages = find_packages(),
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
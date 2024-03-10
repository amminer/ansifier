# export ImageFilePrinter - main purpose of this whole package
from .src.image_printer import ImageFilePrinter

# facilitate tests and stuff
from os import path
PACKAGE_ROOT = path.dirname(path.abspath(__file__))


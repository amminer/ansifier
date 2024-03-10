# export ImageFilePrinter and friends
from .src.image_printer import ImageFilePrinter
from .src.config import UTF8_DEFAULT_CHARS, UTF8_BLOCK_CHARS, ASCII_DEFAULT_CHARS

# facilitate tests and stuff
from os import path
PACKAGE_ROOT = path.dirname(path.abspath(__file__))


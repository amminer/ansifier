# export ImageFilePrinter and friends
from .ansifier.image_printer import ImageFilePrinter
from .ansifier.config import UTF8_DEFAULT_CHARS, UTF8_BLOCK_CHARS, ASCII_DEFAULT_CHARS

# facilitate tests and stuff
from os import path
PACKAGE_ROOT = path.dirname(path.abspath(__file__))


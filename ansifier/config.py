"""
exposes broadly useful configuration variables
"""


import logging

from PIL.Image import NEAREST, LANCZOS, BILINEAR, BICUBIC, BOX, HAMMING
from sys import stdout


def term_supports_utf8():
    """ may want to improve this eventually """
    return stdout.encoding.lower() == 'utf-8'


LOG_FILENAME = 'ansifier.log'

LOG_LEVEL = logging.INFO # set this to DEBUG to... well...

# use utf-8 if possible, otherwise ascii
UTF8_DEFAULT_CHARS = ['\u2588', '\u2593', '\u2592', '\u2591',
                      '@', '#', '$', '\u2022', '+', ':', '-', ' ']

UTF8_BLOCK_CHARS = ['\u2588', '\u2593', '\u2592', '\u2591', ' ']

ASCII_DEFAULT_CHARS = [chr(219), '@', '#', '$', '+', ':', '-', ' ']

CHARS = UTF8_DEFAULT_CHARS if term_supports_utf8() else ASCII_DEFAULT_CHARS


RESIZE_OPTIONS = {  # command line arg: (PIL param, readable name)
    'n': (NEAREST, 'nearest neighbor'),
    'lz': (LANCZOS, 'Lanczos'),
    'bl': (BILINEAR, 'bilinear interpolation'),
    'bc': (BICUBIC, 'bicubic interpolation'),
    'x': (BOX, 'box'),
    'h': (HAMMING, 'Hamming')
}


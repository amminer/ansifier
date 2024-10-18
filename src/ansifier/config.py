"""
this module exposes widely useful configuration data
"""
# pyright:basic


from PIL.Image import Resampling
from sys import stdout


# use utf-8 if possible, otherwise ascii
UTF8_DEFAULT_CHARS = ['\u2588', '\u2593', '\u2592', '\u2591',
                      '@', '#', '$', '\u2022', '+', ':', '-', ' ']

UTF8_BLOCK_CHARS = ['\u2588', '\u2593', '\u2592', '\u2591', ' ']

ASCII_DEFAULT_CHARS = [chr(219), '@', '#', '$', '+', ':', '-', ' ']

CHARS = UTF8_DEFAULT_CHARS if stdout.encoding == 'utf-8' else ASCII_DEFAULT_CHARS

RESIZE_OPTIONS = {  # command line arg: (PIL param, readable name)
    'n': (Resampling.NEAREST, 'nearest neighbor'),
    'lz': (Resampling.LANCZOS, 'Lanczos'),
    'bl': (Resampling.BILINEAR, 'bilinear interpolation'),
    'bc': (Resampling.BICUBIC, 'bicubic interpolation'),
    'x': (Resampling.BOX, 'box'),
    'h': (Resampling.HAMMING, 'Hamming')
}

RESET_ESCAPE = "\033[38;2;255;255;255m"

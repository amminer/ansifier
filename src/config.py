"""
exposes broadly useful configuration variables
"""


from sys import stdout


def term_supports_utf8():
    """ may want to improve this eventually """
    return stdout.encoding.lower() == 'utf-8'


LOG_FILENAME = 'asciifier.log'

# use utf-8 if possible, otherwise ascii
UTF8_DEFAULT_CHARS = ['\u2588', '\u2593', '\u2592', '\u2591',
                      '@', '#', '$', '\u2022', '+', ':', '-', ' ']

ASCII_DEFAULT_CHARS = [chr(219), '@', '#', '$', '+', ':', '-', ' ']

CHARS = UTF8_DEFAULT_CHARS if term_supports_utf8() else ASCII_DEFAULT_CHARS


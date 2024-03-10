"""
Tests whether logging to file appears to be working
"""


import os
from logging import DEBUG

from asciifier import ImageFilePrinter, PACKAGE_ROOT


TEST_IMAGE_PATH = f'{PACKAGE_ROOT}/images-examples/catClout.png'

LOG_PATH = f'{PACKAGE_ROOT}/tests/temp.log'


def test_logging():
    """ 
    Checks:
    * log file was created
    * log file had some data written to it
    DOES NOT check value of contents, but probably should
    TODO
    """
    printer = ImageFilePrinter(TEST_IMAGE_PATH, logfile=LOG_PATH)

    printer.logger.setLevel(DEBUG)
    printer.print_text()

    assert(os.path.exists(LOG_PATH))
    assert(os.path.getsize(LOG_PATH) > 0)

    os.remove(LOG_PATH)


"""
Tests whether logging to file appears to be working,
bare minimum smoke test
"""


import os
from logging import DEBUG

from ansifier import ImageFilePrinter, PACKAGE_ROOT


TEST_IMAGE_PATH = os.path.join(PACKAGE_ROOT, 'images-examples/catClout.png')
LOG_PATH = os.path.join(PACKAGE_ROOT, 'tests/temp.log')


def test_logging():
    """ 
    Checks:
    * log file was created
    * log file had some data written to it
    DOES NOT check value of contents
    """
    printer = ImageFilePrinter(TEST_IMAGE_PATH, logfile=LOG_PATH)

    printer.logger.setLevel(DEBUG)
    printer.print_text()

    assert os.path.exists(LOG_PATH), 'expecting log file to have been created'
    assert os.path.getsize(LOG_PATH) > 0, 'expecting log file to have been written to'

    os.remove(LOG_PATH)


"""
Tests whether the save_to_file appears to be working
"""


import os

from asciifier import ImageFilePrinter, PACKAGE_ROOT


TEST_IMAGE_PATH = f'{PACKAGE_ROOT}/images-examples/catClout.png'
TEST_OUTPUT_TXT_PATH = f'{PACKAGE_ROOT}/tests/temp.txt'


def test_save_to_file():
    """ 
    Checks that:
    * file was created
    * data was written to file
    DOES NOT check file contents for correctness otherwise,
    TODO this would be another test function or even class or file,
    but would be useful
    """
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    printer.save_text(TEST_OUTPUT_TXT_PATH)

    assert(os.path.exists(TEST_OUTPUT_TXT_PATH))
    assert(os.path.getsize(TEST_OUTPUT_TXT_PATH) > 0)

    os.remove(TEST_OUTPUT_TXT_PATH)


"""
Tests whether the save_to_file appears to be working,
bare minimum smoke test
"""


import os

from ansifier import ImageFilePrinter, PACKAGE_ROOT


TEST_IMAGE_PATH = os.path.join(PACKAGE_ROOT, 'images-examples/catClout.png')
TEST_OUTPUT_TXT_PATH = os.path.join(PACKAGE_ROOT, 'tests/temp.txt')


def test_saves_to_file():
    """ 
    Checks that:
    * file was created
    * data was written to file
    DOES NOT check file contents for correctness otherwise
    """
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    printer.save_text(TEST_OUTPUT_TXT_PATH)

    assert os.path.exists(TEST_OUTPUT_TXT_PATH), 'expecting output file to have been created'
    assert os.path.getsize(TEST_OUTPUT_TXT_PATH) > 0, 'expecting output file to contain data'

    os.remove(TEST_OUTPUT_TXT_PATH)


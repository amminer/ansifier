"""
Tests whether using the supported public interface to ImageFilePrinter
incorrectly results in program crashes or other unintended behavior
"""


import os
from copy import deepcopy

from ansifier.ansifier import ImageFilePrinter


TEST_IMAGE_PATH = 'images-examples/catClout.png'


def test_unload_then_generate_output():
    """ 
    Checks that nothing happens when generate_output is called without
    an image object in memory
    """
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    printer.load_image()
    printer.unload_image()

    printer_copy = deepcopy(printer)

    printer.generate_output()

    assert printer_copy == printer


"""
Tests whether the save_to_file feature creates a file.
"""


import os

from asciifier.image_printer_go_brrr import ImageFilePrinter


def test_save_to_file():
    """ 
    Does not actually check its contents, just that it is created and has data.
    """
    filename = 'test.txt'
    printer = ImageFilePrinter('./example-images/catClout.png')
    printer.save_text(filename)
    assert(os.path.exists(filename))
    assert(os.path.getsize(filename) > 0)
    os.remove(filename)


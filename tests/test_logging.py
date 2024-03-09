"""
Tests whether logging to file works
"""


import os
from logging import DEBUG

from asciifier.image_printer_go_brrr import ImageFilePrinter


def test_logging():
    """ 
    Does not actually check its contents, just that it is created and has data.
    """
    logpath = 'test.log'
    printer = ImageFilePrinter('./example-images/catClout.png', logfile=logpath)
    printer.logger.setLevel(DEBUG)
    printer.print_text()

    assert(os.path.exists(logpath))
    assert(os.path.getsize(logpath) > 0)
    os.remove(logpath)


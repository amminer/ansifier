"""
Tests whether writing to standard output is working,
bare minimum smoke test
"""


import os
from subprocess import run, PIPE

from asciifier import ImageFilePrinter, PACKAGE_ROOT


TEST_IMAGE_PATH = os.path.join(PACKAGE_ROOT, 'images-examples/catClout.png')
SCRIPT_PATH = os.path.join(PACKAGE_ROOT, 'image_printer_go_brrr.py')


def test_prints_to_stdout():
    """ 
    Checks that something was written to stdout
    DOES NOT check output for correctness otherwise
    """
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    proc = run([SCRIPT_PATH, TEST_IMAGE_PATH], stdout=PIPE, stdin=PIPE)

    assert proc.stdout


"""
Tests whether writing to standard output is working,
bare minimum smoke test
"""


import os
from subprocess import run, PIPE


TEST_IMAGE_PATH = 'images-examples/catClout.png'
SCRIPT_PATH = 'ansifier.py'


def test_prints_to_stdout():
    """ 
    Checks that something was written to stdout
    DOES NOT check output for correctness otherwise
    """
    proc = run([SCRIPT_PATH, TEST_IMAGE_PATH], stdout=PIPE, stdin=PIPE)
    assert proc.stdout



"""
Tests whether ImageFilePrinter produces output with the correct character set.
Tests main logic, but not CLI... this is a little tricky to organize correctly.
It may be that I should do two sets of tests,
one which produces output by using the class 
and one which goes all the way out to the CLI
for each feature like this, instead of trying to put all the CLI tests
in their own organizational unit...
"""


import pytest
import os
from io import StringIO
from unittest import TestCase
from contextlib import redirect_stdout

from ansifier.ansifier import ImageFilePrinter
from ansifier.config import CHARS


TEST_IMAGE_PATH = 'images-examples/catClout.png'


def test_default_charset():
    printer = ImageFilePrinter(TEST_IMAGE_PATH, max_width=20)

    captured_output = StringIO()
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    with redirect_stdout(captured_output):
        printer.print_text()

    assert all(char in CHARS for char in captured_output)


def test_custom_charset():
    custom_charset = ['@', '#', '$', '%', '*', '^', '\'']
    printer = ImageFilePrinter(TEST_IMAGE_PATH, max_width=20, chars=custom_charset)

    captured_output = StringIO()
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    with redirect_stdout(captured_output):
        printer.print_text()

    assert all(char in custom_charset for char in captured_output)

def test_invalid_charset():
    custom_charset = ['abc', 'def']
    error_message = "composed of 1-length elements"

    with pytest.raises(ValueError) as e:
        printer = ImageFilePrinter(TEST_IMAGE_PATH, max_width=20, chars=custom_charset)
        print(printer.chars)
    assert error_message in str(e)

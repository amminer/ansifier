"""
Tests whether writing to standard output is working,
bare minimum smoke test
"""


from io import StringIO
from contextlib import redirect_stdout

from ansifier.ansifier import ImageFilePrinter


TEST_IMAGE_PATH = 'images-examples/catClout.png'


def test_prints_to_stdout():
    """ 
    Checks that something was written to stdout
    DOES NOT check output for correctness otherwise
    """
    captured_output = StringIO()
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    with redirect_stdout(captured_output):
        printer.print_text()

    assert captured_output.getvalue()


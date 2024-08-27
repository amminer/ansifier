"""
Tests whether html output is working as expected
in the most basic case
kind of a smoke test
"""

from io import StringIO
from contextlib import redirect_stdout
from difflib import SequenceMatcher

from ansifier.ansifier import ImageFilePrinter


TEST_IMAGE_PATH = 'images-examples/catClout.png'
expected_output_file = 'tests/expected.html'
with open(expected_output_file, 'r') as rf:
    expected_output = rf.read()


def test_html_output():
    """ 
    Checks that something was written to stdout
    DOES NOT check output for correctness otherwise
    """
    captured_output = StringIO()
    printer = ImageFilePrinter(TEST_IMAGE_PATH, output_format='html/css', max_height=20)

    with redirect_stdout(captured_output):
        printer.print_text()
    observed_output = captured_output.getvalue()

    print(f'output matches {SequenceMatcher(a=expected_output, b=observed_output).ratio() * 100}%')
    assert observed_output == expected_output


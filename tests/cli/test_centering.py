#pyright: basic


from difflib import SequenceMatcher
from os import path
from subprocess import check_output

from tests.template_cli import cli_test


test_image_path = 'images-examples/catClout.png'


def test_cli_centering_horizontal(request):
    """ 
    process image file, check ansi output
    """
    expected_output_file = 'tests/expected_center_horizontally.txt'
    cli_test(request, test_image_path, expected_output_file, output_format='ansi-escaped',
             center_horizontally=None, height=10, width=30)


def test_cli_centering_vertically(request):
    """ 
    process image file, check ansi output
    """
    expected_output_file = 'tests/expected_center_vertically.txt'
    cli_test(request, test_image_path, expected_output_file, output_format='ansi-escaped',
             center_vertically=None, height=10, width=30)

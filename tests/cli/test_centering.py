#pyright: basic
#TODO figure out how to mock terminal size


from difflib import SequenceMatcher
from os import path
from subprocess import check_output

from tests.template_cli import cli_test


test_image_path = 'images-examples/catClout.png'


def test_cli_centering_horizontal(request):
    expected_output_file = 'tests/expected_center_horizontally.txt'
    cli_test(request, test_image_path, expected_output_file, output_format='ansi-truecolor',
             center_horizontally=None, height=20, width=20)


def test_cli_centering_vertically(request):
    expected_output_file = 'tests/expected_center_vertically.txt'
    cli_test(request, test_image_path, expected_output_file, output_format='ansi-truecolor',
             center_vertically=None, height=20, width=20)

def test_cli_centering_both(request):
    expected_output_file = 'tests/expected_center_both.txt'
    cli_test(request, test_image_path, expected_output_file, output_format='ansi-truecolor',
             center_horizontally=None, center_vertically=None, height=20, width=20)

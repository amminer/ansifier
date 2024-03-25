"""
Test whether ImageFilePrinter can be used at the most basic level without blowing up,
bare naked minimum smoke test, no assertions, just run the code
"""


import os
import pytest
from PIL import Image

from ansifier import ImageFilePrinter, PACKAGE_ROOT


TEST_IMAGE_PATH = os.path.join(PACKAGE_ROOT, 'images-examples/catClout.png')
TEST_GIF_PATH = os.path.join(PACKAGE_ROOT, 'images-examples/hmmm.gif')


def test_can_consume_ImageFilePrinter():
    """ basic usage """
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    printer.print_text()


def test_can_pass_params_to_ImageFilePrinter():
    """
    custom usage
    each init parameter warrants its own tests eventually
    """
    printer = ImageFilePrinter(TEST_IMAGE_PATH,
        max_height=20,
        max_width=20,
        resize_method=Image.BICUBIC,
        char_by_brightness=True,
        chars=['\'', '"', '*', '%', '#'],
        animate=0)

    printer.print_text()


def test_can_run_animation_on_gif():
    """ basic usage """
    printer = ImageFilePrinter(TEST_GIF_PATH,
            max_width=10,
            max_height=10,
            animate=1)

    printer.print_text()


def test_negative_must_pass_image_path():
    """ ensure that you can't instantiate without a path """
    error_message = "missing 1 required positional argument: 'image_path'"

    with pytest.raises(TypeError) as e:
        printer = ImageFilePrinter(animate=20)
        printer.print_text()
    assert error_message in str(e)

    with pytest.raises(TypeError) as e:
        init_args_printer = ImageFilePrinter(
            max_height=20,
            max_width=20,
            resize_method=Image.BICUBIC,
            char_by_brightness=True,
            chars=['\'', '"', '*', '%', '#'],
            animate=0)
        init_args_printer.print_text()
    assert error_message in str(e)


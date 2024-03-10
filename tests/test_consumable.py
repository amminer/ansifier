"""
Test whether ImageFilePrinter can be imported and used without blowing up.
Pretty much the bare naked minimum smoke test.
"""


from PIL import Image

from asciifier import ImageFilePrinter, PACKAGE_ROOT


TEST_IMAGE_PATH = f'{PACKAGE_ROOT}/images-examples/catClout.png'


def test_can_consume_ImageFilePrinter():
    """ basic usage """
    printer = ImageFilePrinter(TEST_IMAGE_PATH)

    printer.print_text()


def test_can_pass_params_to_ImageFilePrinter():
    """ custom usage """
    printer = ImageFilePrinter(TEST_IMAGE_PATH,
        max_height=20,
        max_width=20,
        resize_method=Image.BICUBIC,
        char_by_brightness=True,
        chars=['\'', '"', '*', '%', '#'],
        animate=0)

    printer.print_text()


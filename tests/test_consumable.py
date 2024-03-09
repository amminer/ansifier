"""
Test whether ImageFilePrinter can be imported and used without blowing up
not at all comprehensive (yet?).
"""


from PIL import Image

from asciifier.image_printer_go_brrr import ImageFilePrinter


def test_can_consume_ImageFilePrinter():
    """ basic usage """
    printer = ImageFilePrinter('./example-images/catClout.png')
    printer.print_text()


def test_can_pass_params_to_ImageFilePrinter():
    """ custom usage """
    printer = ImageFilePrinter('./example-images/catSwag.png',
        max_height=20,
        max_width=20,
        resize_method=Image.BICUBIC,
        char_by_brightness=True,
        chars=['\'', '"', '*', '%', '#'],
        animate=0)
    printer.print_text()


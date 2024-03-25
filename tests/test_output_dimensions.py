"""
Tests whether ImageFilePrinter produces output within the requested dimensions
for images with landscape, portrait, and square aspect ratios.
Could use inheritance for test classes but would probably be overwrought
"""


import os
from unittest import TestCase

from ansifier import ImageFilePrinter, PACKAGE_ROOT


class TestSquare(TestCase):
    image_path = os.path.join(PACKAGE_ROOT, 'images-examples/catSwag.png')

    def test_width_square(self):
        """ 
        Checks that output is exactly the requested maximum width for images
        with square aspect ratios
        """
        printer = ImageFilePrinter(self.image_path, max_width=20)
        assert printer.output_width == 20

    def test_height_square(self):
        """ 
        Checks that output is exactly the requested maximum height for images
        with square aspect ratios
        """
        printer = ImageFilePrinter(self.image_path, max_height=20)
        assert printer.output_height == 20


class TestWide(TestCase):
    image_path = os.path.join(PACKAGE_ROOT, 'images-examples/loaf.gif')

    def test_width_wide(self):
        """ 
        Checks that output is within the requested maximum width for images
        with wide aspect ratios
        """
        printer = ImageFilePrinter(self.image_path, max_width=20)
        assert printer.output_width <= 20

    def test_height_wide(self):
        """ 
        Checks that output is within the requested maximum height for images
        with wide aspect ratios
        """
        printer = ImageFilePrinter(self.image_path, max_height=20)
        assert printer.output_height <= 20


class TestTall(TestCase):
    image_path = os.path.join(PACKAGE_ROOT, 'images-examples/miku.gif')

    def test_width_tall(self):
        """ 
        Checks that output is within the requested maximum width for images
        with tall aspect ratios
        """
        printer = ImageFilePrinter(self.image_path, max_width=20)
        assert printer.output_width <= 20

    def test_height_tall(self):
        """ 
        Checks that output is within the requested maximum height for images
        with tall aspect ratios
        """
        printer = ImageFilePrinter(self.image_path, max_height=20)
        assert printer.output_height <= 20


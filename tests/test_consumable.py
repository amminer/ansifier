"""
Package can be used at the most basic level without blowing up,
bare minimum functional tests, no assertions, just run the code
"""


import pytest

from ansifier.ansify import ansify


TEST_IMAGE_PATH = 'images-examples/catClout.png'
TEST_GIF_PATH = 'images-examples/hmmm.gif'


def test_can_consume_package():
    print(ansify(TEST_IMAGE_PATH))


def test_can_pass_params():
    """
    hit non-defaults for each param, each init parameter may warrant its own tests eventually
    and more careful exhaustion of possible combinations may be warranted
    """
    print(ansify(
        TEST_IMAGE_PATH,
        chars=['\'', '"', '*', '%', '#'],
        height=20,
        width=20,
        by_intensity=True,
        animate=False,
        output_format='html/css'))


def test_negative_must_pass_image_path():
    """ ensure that you can't instantiate without a path """
    error_message = "missing 1 required positional argument: 'image_path'"

    with pytest.raises(TypeError) as e:
        ansify(animate=20)  # pyright:ignore
    assert error_message in str(e)

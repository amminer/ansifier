"""
Package can be used at the most basic level without blowing up,
bare minimum functional tests, no assertions, just run the code
"""
# pyright:basic


from ansifier.ansify import ansify


TEST_IMAGE_PATH = 'images-examples/catClout.png'
TEST_GIF_PATH = 'images-examples/hmmm.gif'


def test_can_consume_package(request):
    """
    ensures that import and usage are working in the most basic sense,
    also checks whether ansifier reads image inputs as expected
    """
    if request.config.getoption('--from-installed'):
        from ansifier import ansify
    else:
        from ansifier.ansify import ansify
    output = ansify(TEST_IMAGE_PATH)
    assert(output)
    assert(output[0])


def test_can_pass_params(request):
    """
    hit non-defaults for each param, each init parameter may warrant its own tests eventually
    and more careful exhaustion of possible combinations may be warranted
    """
    if request.config.getoption('--from-installed'):
        from ansifier import ansify
    else:
        from ansifier.ansify import ansify
    print(ansify(
        TEST_IMAGE_PATH,
        chars=['\'', '"', '*', '%', '#'],
        height=20,
        width=20,
        by_intensity=True,
        animate=True,
        output_format='html/css'))

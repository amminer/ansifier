#pyright: basic


from tests.template_io import io_test


test_image_path = 'images-examples/catClout.png'
expected_output_file = 'tests/expected.html'

def test_html_output(request):
    """ 
    process image file, check html output
    """
    io_test(request, test_image_path, expected_output_file, output_format='html/css', height=50)

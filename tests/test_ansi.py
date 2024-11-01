#pyright: basic


from tests.template_io import io_test


test_image_path = 'images-examples/catClout.png'
expected_output_file = 'tests/expected.txt'
observed_output_file = 'log/observed.txt'

def test_ansi_output(request):
    """ 
    process image file, check ansi output
    """
    io_test(request,
            test_image_path=test_image_path,
            expected_output_file=expected_output_file,
            observed_output_file=observed_output_file,
            output_format='ansi-escaped', height=50)

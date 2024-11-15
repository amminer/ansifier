#pyright: basic


from tests.template_io import io_test


test_image_path = 'images-examples/catClout.png'

def test_ansi_truecolor(request):
    """ 
    process image file, check ansi output
    """
    expected_output_file = 'tests/expected_truecolor.txt'
    observed_output_file = 'log/observed_truecolor.txt'
    io_test(request,
            test_image_path=test_image_path,
            expected_output_file=expected_output_file,
            observed_output_file=observed_output_file,
            output_format='ansi-truecolor', height=50)

def test_ansi_256color(request):
    """ 
    process image file, check ansi output
    """
    expected_output_file = 'tests/expected_256color.txt'
    observed_output_file = 'log/observed_256color.txt'
    io_test(request,
            test_image_path=test_image_path,
            expected_output_file=expected_output_file,
            observed_output_file=observed_output_file,
            output_format='ansi-256', height=50)

def test_ansi_16color(request):
    """ 
    process image file, check ansi output
    """
    expected_output_file = 'tests/expected_16color.txt'
    observed_output_file = 'log/observed_16color.txt'
    io_test(request,
            test_image_path=test_image_path,
            expected_output_file=expected_output_file,
            observed_output_file=observed_output_file,
            output_format='ansi-16', height=50)

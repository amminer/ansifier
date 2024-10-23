#pyright: basic


from tests.template_io import io_test


test_image_path = 'images-examples/catWizard.mp4'
expected_output_file = 'tests/expected_mp4.txt'

def test_video_input(request):
    """ 
    process video file, check ansi output
    """
    io_test(request, test_image_path, expected_output_file, output_format='ansi-escaped', height=50)

#pyright: basic


import logging
import pytest

from tests.template_io import io_test


logger = logging.getLogger()
test_image_path = 'images-examples/catWizard.mp4'
expected_output_file = 'tests/expected_mp4.txt'

@pytest.mark.requires_opencv
def test_video_input(request):
    """ 
    process video file, check ansi output
    """
    try:
        import cv2
    except ImportError:
        pytest.skip('test requires OS-installed opencv object files')
    io_test(request, test_image_path, expected_output_file, output_format='ansi-escaped', height=50)


def test_video_input_with_no_sys_opencv(request):
    """ 
    process video file, check ansi output
    """
    try:
        import cv2
        pytest.skip('test requires that opencv not be installed at OS level')
    except ImportError:
        with pytest.raises(Exception, match='try installing python3-opencv'):
            io_test(request, test_image_path, expected_output_file, output_format='ansi-escaped', height=50)

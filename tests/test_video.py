from difflib import SequenceMatcher

from ansifier.ansify import ansify


TEST_IMAGE_PATH = 'images-examples/catWizard.mp4'
expected_output_file = 'tests/expected_mp4.txt'
with open(expected_output_file, 'r') as rf:
    expected_output = rf.read()


def test_video_input():
    """ 
    Basic check that ansifier can process video files
    """
        
    observed_output = ansify(TEST_IMAGE_PATH, output_format='ansi-escaped', height=50)[0]

    print(f'output matches {SequenceMatcher(a=expected_output, b=observed_output).ratio() * 100}%')
    print(f'expected\n{expected_output}')
    print(f'observed\n{observed_output}')
    assert observed_output == expected_output


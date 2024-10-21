from difflib import SequenceMatcher

from ansifier.ansify import ansify


TEST_IMAGE_PATH = 'images-examples/catClout.png'
expected_output_file = 'tests/expected.html'
with open(expected_output_file, 'r') as rf:
    expected_output = rf.read()


def test_html_output():
    """ 
    Basic check that ansifier produces expected output for html format
    """
        
    observed_output = ansify(TEST_IMAGE_PATH, output_format='html/css', height=50)[0]

    sequence_matcher = SequenceMatcher(a=expected_output, b=observed_output)
    print(f'output matches {sequence_matcher.ratio() * 100}%')
    assert observed_output == expected_output


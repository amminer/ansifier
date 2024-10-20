from difflib import SequenceMatcher

from ansifier.ansify import ansify


TEST_IMAGE_PATH = 'images-examples/catClout.png'
expected_output_file = 'tests/expected.txt'
with open(expected_output_file, 'r') as rf:
    expected_output = rf.read()


def test_html_output():
    """ 
    Checks that something was written to stdout
    DOES NOT check output for correctness otherwise
    """
        
    observed_output = ansify(TEST_IMAGE_PATH, output_format='ansi-escaped', height=50)[0]

    print(f'output matches {SequenceMatcher(a=expected_output, b=observed_output).ratio() * 100}%')
    print(f'expected\n{expected_output}')
    print(f'observed\n{observed_output}')
    assert observed_output == expected_output


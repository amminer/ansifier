#pyright: basic


from difflib import SequenceMatcher

from ansifier.ansify import ansify


def io_test(request, test_image_path, expected_output_file, output_format):
    with open(expected_output_file, 'r') as rf:
        expected_output = rf.read()
        
    observed_output = ansify(test_image_path, output_format=output_format, height=50)[0]

    if request.config.getoption('--regenerate-expectations'):
        with open(expected_output_file, 'w') as wf:
            wf.write(observed_output)

    print(f'output matches {SequenceMatcher(a=expected_output, b=observed_output).ratio() * 100}%')
    print(f'expected\n{expected_output}')
    print(f'observed\n{observed_output}')
    assert observed_output == expected_output


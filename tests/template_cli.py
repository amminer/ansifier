#pyright: basic


from difflib import SequenceMatcher
from os import path
from subprocess import check_output


def cli_test(request, test_image_path, expected_output_file, **kwargs):
    """ need to look into where terminal dimensions are coming from in here """
    if not path.exists(expected_output_file):
        with open(expected_output_file, 'w') as wf:
            wf.write('')
    with open(expected_output_file, 'r') as rf:
        expected_output = rf.read()

    args = ['python', '-m', 'ansifier.cli', test_image_path]
    for k, v in kwargs.items():
        args.append(f'--{k.replace("_", "-")}')
        if v is not None:
            args.append(str(v))
    print('executing', ' '.join(args))
    observed_output = check_output(args=args).decode('utf-8')

    if request.config.getoption('--regenerate-expectations'):
        with open(expected_output_file, 'w') as wf:
            wf.write(observed_output)

    print(f'output matches {SequenceMatcher(a=expected_output, b=observed_output).ratio() * 100}%')
    print(f'expected from {expected_output_file}\n{expected_output}')
    print(f'observed from {test_image_path}\n{observed_output}')
    assert observed_output == expected_output


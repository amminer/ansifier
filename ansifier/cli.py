"""
entry point for use from a shell;
invoke this module i.e. python -m src.ansifier.cli
"""
# pyright: basic
import argparse
import re

from colorama import just_fix_windows_console
from importlib.metadata import version
from os.path import dirname
from shutil import get_terminal_size
from sys import version_info
from time import sleep

from .config import CHARLISTS
from .input_formats import INPUT_FORMATS
from .output_formats import OUTPUT_FORMATS
from .ansify import ansify


input_formats = list(INPUT_FORMATS.keys())
output_formats = list(OUTPUT_FORMATS.keys())


def main():
    argparser = argparse.ArgumentParser(
        prog='ansifier',
        description='Takes an image file as input and '
        'prints a unicode representation of the image to the terminal.')

    argparser.add_argument('-v', '--version', action='store_true',
        required=False, default=False, help='print version information and exit')

    argparser.add_argument('-H', '--height', action='store', type=int,
        required=False, default=0,
        help='Restrict output to this many rows. '
             'By default, restricts output to the height of the calling shell\'s terminal, '
             'minus one to account for the prompt line. Multiline prompts not yet considered.')

    argparser.add_argument('-W', '--width', action='store', type=int,
        required=False, default=0,
        help='Restrict output to twice this many columns (it takes ~2 chars to represent a square). '
             'By default, restricts output to the width of the calling shell\'s terminal.')

    charlists = ''.join(f'"{k}": "{",".join(v)}" ' for k,v in CHARLISTS.items())
    argparser.add_argument('-c', '--chars', action='store', type=str,
        required=False, default=",".join(CHARLISTS["default"]), help='comma-separated sequence of characters '
        'to be chosen from when converting regions of the image to text. Should be sorted from '
        f'more opaque to less opaque in normal usage.'
        f'There are a few special values for this argument: [{charlists}]')

    argparser.add_argument('-f', '--input-format', action='store',
            type=str, required=False, default='', help='mimetype of file being '
                'provided as input; must be one of the following: '
                f'{input_formats}. By default, tries to guess, falling back on {input_formats[0]}.')

    argparser.add_argument('-F', '--output-format', action='store',
            type=str, required=False, default=output_formats[0], help='how to '
                'format output text - must be one of the following: '
                f'{output_formats}. Default is {output_formats[0]}.')

    argparser.add_argument('-a', '--animate', action='store',
        required=False, type=int, default=0,
        help='If the input image is animated (.gif), process all keyframes and '
            'print them with ANIMATE milliseconds of delay between frames.')

    argparser.add_argument('-L', '--loop-infinitely', action='store_true',
        required=False, default=False,
        help='With -a, causes the animation to loop until the '
        'program is terminated.')

    argparser.add_argument('-i', '--char-by-intensity', action='store_true',
        required=False, default=False, help='Use intensity (instead of '
            'transparency) to determine character used to represent an input region.')

    argparser.add_argument('-I', '--invert-char-selection', action='store_true',
        required=False, default=False,
        help='Invert the effect of transparency (or intensity when using -i) '
            'on char selection; useful for images with '
            'dark foregrounds and bright backgrounds, for example.')

    argparser.add_argument('-z', '--center-horizontally', action='store_true',
        required=False, default=False,
        help='Use terminal size to center output horizontally, for ansi-escaped output only')

    argparser.add_argument('-V', '--center-vertically', action='store_true',
        required=False, default=False,
        help='Use terminal size to center output vertically, for ansi-escaped output only')

    argparser.add_argument('image_path', nargs='?', default=None)

    args = argparser.parse_args()

    if args.version:
        print('ansifier', version('ansifier'), 'from',
            dirname(__file__),
            f'(python {version_info[0]}.{version_info[1]})')
        exit(0)

    if args.image_path is None:
        argparser.error('the following arguments are required: image_path')

    terminal_height = get_terminal_size().lines
    terminal_width = get_terminal_size().columns

    if args.height == 0:
        args.height = terminal_height - 1
    if args.width == 0:
        args.width = terminal_width

    if args.chars in CHARLISTS.keys():
        args.chars = CHARLISTS[args.chars]
    else:
        args.chars=list(args.chars.split(','))

    if args.invert_char_selection:
        args.chars = args.chars[-1::-1]


    just_fix_windows_console()
    output = ansify(
        args.image_path,
        chars=args.chars,
        height=args.height,
        width=args.width,
        by_intensity=args.char_by_intensity,
        input_format=args.input_format,
        output_format=args.output_format,
        animate=args.animate)

    if args.output_format == output_formats[0]\
    and args.center_horizontally or args.center_vertically:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')  # TODO don't *need* re
        output_width = len(ansi_escape.sub('', output[0].split('\n')[0]))
        output_height = output[0].count('\n')
        h_pad = ' ' * ((terminal_width - output_width) // 2)
        v_pad = '\n' * ((terminal_height - output_height) // 2)

        for i, frame in enumerate(output):
            if args.center_horizontally and output_width + 2 < terminal_width:
                lines = frame.split('\n')
                for j, line in enumerate(lines[:-1]):
                    lines[j] = h_pad + line + h_pad
                frame = '\n'.join(lines)
                output[i] = frame

            if args.center_vertically and output_height + 2 < terminal_height:
                output[i] = v_pad + output[i] + v_pad

    interval = args.animate/1000.0
    done = False
    loop = args.loop_infinitely
    while not done:
        for frame in output:
            print(frame, end='')
            sleep(interval)  # TODO account for print overhead
        if not loop:
            done = True


if __name__ == '__main__':
    main()

#!/bin/python3


"""
See -h
A bit of a scrappy, hacked up little script, at least for now.
* Steals output from neofetch --off
* generates ansi art from the image, takes terminal size into account
* combines these outputs and prints it all

# TODO XDG_CONFIG
image printed defaults to $HOME/Pictures/meofetch-art.png;
if this image does not exist and no alternative is passed to the command, exits
"""


import os
import re

from shutil import get_terminal_size
from sys import argv, path
from subprocess import check_output
from cli import run_cli, get_parser

from config import CHARS, RESIZE_OPTIONS
from image_printer import ImageFilePrinter, length_after_processing


homedir = os.environ['HOME']
# TODO XDG_CONFIG
DEFAULT_IMAGE_PATH = str(os.path.join(homedir, 'Pictures/meofetch-art.png'))
# TODO flesh these args out and work them into the ones from get_parser
LEFT_PADDING = -1  # -1 for center
#LEFT_PADDING = 8  # more traditional
BETWEEN_PADDING = 7


def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def length_after_processing(text):
    processed_text = remove_ansi_escape_sequences(text)
    return len(processed_text)


# get terminal dimensions
sz = get_terminal_size()
w_orig = sz[0]
h = sz[1] - 1  # prompt

# get output from neofetch
system_info = check_output(['neofetch', '--off']).decode('UTF-8')
#system_info = os.popen('neofetch --off').read()  # Terminal: meofetch.py lol
sysinfo_lines = system_info.split('\n')
sysinfo_lines = [' '*BETWEEN_PADDING + l for l in sysinfo_lines]

# take lines off the bottom of neofetch's output until the output will fit in the terminal
while h < len(sysinfo_lines):
    sysinfo_lines.pop()
# TODO de-prioritize neofetch lines for screen space vs. ansi art here?

# Account for horizonal room for neofetch output
w = (w_orig - max(list(map(length_after_processing, sysinfo_lines)))) - 6

# override this part of the cli
parser = get_parser()
# alter help message
# hack up the internal optiosn for now TODO parser subclass?
image_path_action = [a for a in parser._actions if a.dest == 'image_path'][0]
image_path_action.required = False
image_path_action.default = DEFAULT_IMAGE_PATH
for helparg in parser._actions[0].option_strings:
    if helparg in argv:
        print('meofetch takes output from the script below and interleaves it '
            'with neofetch system info, with some padding.\n'
            'if the terminal isn\'t large enough, neofetch lines may be '
            'trimmed from the bottom, and/or the ansi image may not display.\n'
            'Note that if no image file is provided, meofetch defaults to use '
            '$HOME/Pictures/meofetch-art.png. If $HOME is undefined and no '
            'path is provided, meofetch will not work.\n'  # TODO XDG_CONFIG
            'Note that the --animate option has no affect here.'
            'Note that using --center-horizontally in this context is '
            'discouraged.\n'
            'Finally, note that --max-width and --max-height may only reduce '
            'the output dimensions from those found based on terminal size.\n')

if w > 0 and h > 0:

    args = parser.parse_args()

    if not args.image_path and not os.environ['HOME']:
        print('No image path provided and HOME env var not defined, see meofetch -h')
        exit(1)

    args.animate = 0

    if args.max_width is not None:
        args.max_width = min(args.max_width, w)
    else:
        args.max_width = w

    if args.max_height is not None:
        args.max_height = min(args.max_height, h) if args.max_width is not None else h
    else:
        args.max_height = h

    # the .output attr was not originally intended as a public interface,
    #  but it sure works as one
    ansi_art = run_cli(args).output
    ansi_lines = ansi_art.split('\n')[:-1]
    max_ansi_line_len = max(list(map(length_after_processing, ansi_lines)))
    # pad left
    if LEFT_PADDING != -1:
        ansi_lines = [' '*LEFT_PADDING + line for line in ansi_lines]
    else:  # center ansi output horizontally
        # get the longest total line...
        longest_output_line = max(map(length_after_processing,
            [l1+l2 for l1, l2 in zip(ansi_lines, sysinfo_lines)]))
        LEFT_PADDING = (w_orig - longest_output_line) // 2
        ansi_lines = [' '*LEFT_PADDING + line for line in ansi_lines]  # TODO
else:
    ansi_lines = []
    max_ansi_line_len = 0

# ensure neofetch output does not unindent if it has more rows than ansi art
# also centers ansi art in this case
# TODO use a generator to alternate padding direction?
i = 0
padding_row = ' ' * (max_ansi_line_len + LEFT_PADDING)
while len(sysinfo_lines) > len(ansi_lines):
    if i % 2:
        ansi_lines.insert(0, padding_row)
    else:
        ansi_lines.append(padding_row)
    i += 1

# ensure neofetch output is centered when ansi art has more rows
# TODO this is repeated in cli.py almost exactly
difference = len(ansi_lines) - len(sysinfo_lines) + 2
pad_num = difference // 2
pad = [' ' for i in range(pad_num)]
sysinfo_lines = pad + sysinfo_lines + pad

for ansi_line, sysinfo_line in zip(ansi_lines, sysinfo_lines):
    # ensure no ansi lines are shorter
    #  seemingly due to how ansifier works... TODO?
    ansi_line = ansi_line.ljust(max_ansi_line_len)
    print(ansi_line, sysinfo_line)

# This is necessary due to something about the output
#  from neofetch... but why??? Something about cooked vs raw chars?
print(os.popen('tput cnorm').read(), end='')
print(os.popen('setterm --linewrap on').read(), end='')


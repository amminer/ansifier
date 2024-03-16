#!/bin/python3


"""
A scrappy, hacked up little script, at least for now.
* Steals output from neofetch --off
* generates ascii art from the image whose path is passed as
  the first command line argument, takes terminal size into account
* combines these outputs into my own strange fetch and prints it
"""


import os
import re
import subprocess

from shutil import get_terminal_size
from sys import argv, path


# TODO flesh this out, give it more arguments,
#  maybe its own repo which might be an insane idea
#  like can I really write a fetch that just steals from neofetch?
#  Should I just fork neofetch so it's separately configurable?
#  is that even a little bit realistic?
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
system_info = subprocess.check_output(['neofetch', '--off']).decode('UTF-8')
#system_info = os.popen('neofetch --off').read()  # Terminal: meofetch.py lol
sysinfo_lines = system_info.split('\n')
sysinfo_lines = [' '*BETWEEN_PADDING + l for l in sysinfo_lines]

# read in a custom image if provided, otherwise the default on the next line
image_path = '/home/meelz/Pictures/meofetch-art.png'
try:
    if argv[1] and os.path.exists(argv[1]):
        image_path = argv[1]
except:
    pass

# take lines off the bottom of neofetch's output until the output will fit in the terminal
while h < len(sysinfo_lines):
    sysinfo_lines.pop()

# Account for horizonal room for neofetch output
w = (w_orig - max(list(map(length_after_processing, sysinfo_lines)))) // 2 - 6

if w > 0 and h > 0:
# the .output attr was not originally intended as a public interface,
#  but it sure works as one
#from src.image_printer import ImageFilePrinter
#from asciifier import ImageFilePrinter
# That won't work until packaging is complete, so this works for now instead on my system,
#  at least for prototyping
#ascii_art = ImageFilePrinter(image_path, max_width=w, max_height=h).output
    ascii_art = subprocess.check_output(
        ['imgprint', '/home/meelz/Pictures/meofetch-art.png', f'-W{w}', f'-H{h}']).decode('UTF-8')
    ascii_lines = ascii_art.split('\n')[:-1]
    max_ascii_line_len = max(list(map(length_after_processing, ascii_lines)))
# pad left
    if LEFT_PADDING != -1:
        ascii_lines = [' '*LEFT_PADDING + line for line in ascii_lines]
    else:  # center ascii output horizontally
        # get the longest total line...
        longest_output_line = max(map(length_after_processing,
            [l1+l2 for l1, l2 in zip(ascii_lines, sysinfo_lines)]))
        LEFT_PADDING = (w_orig - longest_output_line) // 2
        ascii_lines = [' '*LEFT_PADDING + line for line in ascii_lines]  # TODO
else:
    ascii_lines = []
    max_ascii_line_len = 0

# ensure neofetch output does not unindent if it has more rows than ascii art
# also centers ascii art in this case
# TODO use a generator to alternate padding direction?
i = 0
padding_row = ' ' * (max_ascii_line_len + LEFT_PADDING)
while len(sysinfo_lines) > len(ascii_lines):
    if i % 2:
        ascii_lines.insert(0, padding_row)
    else:
        ascii_lines.append(padding_row)
    i += 1

# ensure neofetch output is centered when ascii art has more rows
difference = len(ascii_lines) - len(sysinfo_lines) + 2
pad_num = difference // 2
pad = [' ' for i in range(pad_num)]
sysinfo_lines = pad + sysinfo_lines + pad

for ascii_line, sysinfo_line in zip(ascii_lines, sysinfo_lines):
    # ensure no ascii lines are shorter
    #  seemingly due to how asciifier works... TODO?
    ascii_line = ascii_line.ljust(max_ascii_line_len)
    print(ascii_line, sysinfo_line)

# This is necessary due to something about the output
#  from neofetch... but why??? Something about cooked vs raw chars?
print(os.popen('tput cnorm').read(), end='')
print(os.popen('setterm --linewrap on').read(), end='')


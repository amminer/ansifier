#!/bin/python3
# This only works on Linux (maybe Mac as well)
# just a little example of how you might use the main script

import os

# write this file with image_printer_go_brrr.py
txtpath = './img.txt'
ascii_art = os.popen(f'cat {txtpath}').read()
ascii_lines = ascii_art.split('\n')

system_info = os.popen('neofetch --off').read()
sysinfo_lines = system_info.split('\n')

for ascii_line, sysinfo_line in zip(ascii_lines, sysinfo_lines):
    print(ascii_line, sysinfo_line)

# This is necessary due to something about the output
# from neofetch... but why??? Something about cooked vs raw chars?
print(os.popen('tput cnorm').read(), end='')
print(os.popen('setterm --linewrap on').read(), end='')


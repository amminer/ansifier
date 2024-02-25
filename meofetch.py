import os

# write output from asciifier into this file
txtpath = './img.txt'
ascii_art = os.popen(f'cat {txtpath}').read()
ascii_lines = ascii_art.split('\n')

system_info = os.popen('neofetch --off').read()
sysinfo_lines = system_info.split('\n')

for ascii_line, sysinfo_line in zip(ascii_lines, sysinfo_lines):
    print(ascii_line, sysinfo_line)

# this resets the cursor
print(os.popen('tput cnorm').read())
# but something is still mega borked...
# seems to be related to sysinfo_line, not ascii_line???


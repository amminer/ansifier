"""
 Known bugs (have been tweaking, unsure if still present as of right now):
 at large terminal sizes (very zoomed out) image takes on diamond-shaped
   rgb artifacting?
 at extreme terminal aspect ratios similar artifacting occurs as the image is
   very slightly stretched along the long axis of the terminal window...
 lame and obfuscated behind PIL as these bugs are, this is kinda better than
   the earlier version.
 transparency for nonRGB images turns white, should turn black (Image.convert)
 TODO
 Re-write with classes?
 could effectively increase output "pixel" density by 2x as many column
   samples as row samples?
"""


import argparse
from PIL import Image
from sys import exit
from os import get_terminal_size


CHARS = ['\u2588', '\u2593', '\u2592', '\u2591', '#', '@', '$', '+', '-', ' ']  #UNICODE_ONLY
INTERVALS = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]


def resize_image_to_fit(im, max_height, max_width):
    """
    :param im: PIL.Image, thumbnail method will be used to resize iteratively
        until the largest possible scaled-down dimensions are found
        without losing correct aspect ratio
    :param max_height: int, maximum number of character-pixels... vertical
        need a better name for visual single-characters in output
    :param max_width: int, maximum number of character-pixels, horizontal
    :return: PIL.Image, scaled down to max size that fits provided dimensions
    """
    resize_method = Image.LANCZOS
    new_height, new_width = max_height, max_width
    problem_dim = max(new_width, new_height)
    im.thumbnail((problem_dim, problem_dim), resize_method)

    while im.size[0] > max_width or im.size[1] > max_height:  # img sz > terminal
        problem_dim = max(new_width, new_height)
        im.thumbnail((problem_dim, problem_dim), resize_method)
        new_height -= 1
        new_width -= 1

    return im

def get_char_from_alpha(a):
    """
    takes in a transparency value and maps it to a character. The idea
    is that the more transparent an image's pixel is, the less "foreground"
    its representative terminal character should have. This is why this
    program is unicode-only... TODO adapt based on runtime environment
    :param a: int, min 0, max 255, alpha value of a pixel
    :return: character fitting alpha value
    """
    for i, interval in enumerate(INTERVALS):
        if a >= interval:
            return CHARS[i]
    return '🚩'  #UNICODE_ONLY


def main(img_path, debug=False):
    """
    get terminal dimensions,
    generate output,
    print output to terminal
    """
    # assume a terminal character is about twice as tall as it is wide
    max_height = get_terminal_size().lines - 1  # -1 accounts for prompt line
    max_width = get_terminal_size().columns // 2
    im = Image.open(img_path).convert("RGBA")
    if debug:
        max_height = max_height/10 * 9
        max_width = max_width/10 * 9
    im = resize_image_to_fit(im, max_height, max_width)

    output = []
    for j in range(im.size[1]):
        for i in range(im.size[0]):  # one iteration for each char in output
            pix = im.getpixel((i, j))
            r = pix[0]
            g = pix[1]
            b = pix[2]
            a = pix[3]
            char = get_char_from_alpha(a)

            output += f"\033[38;2;{r};{g};{b}m{char}" * 2 + "\033[38;2;255;255;255m"
        output += "\n"  # line break at end of each row

    for c in output:
        print(c, end="")

    exit(0)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--debug', action='store_true',
            required=False, default=False,
            help='reduce output dims, may print helpful info')
    argparser.add_argument('imageFilePath')
    args = argparser.parse_args()
    main(args.imageFilePath, args.debug)


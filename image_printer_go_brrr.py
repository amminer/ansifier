"""
 Known bugs (have been tweaking, unsure if still present as of right now):
 * at large terminal sizes (very zoomed out) image takes on diamond-shaped
   rgb artifacting?
 * at extreme terminal aspect ratios similar artifacting occurs as the image is
   very slightly stretched along the long axis of the terminal window...
 TODO
 * This would be really cool if it could be consumed/reused by other programs
   that produce a terminal interface of some kind e.x. curses, whatever -
   it should provide an interface for its options other than command-line args.
 * Re-write with a class or two?
 * Would be cool, but maybe scale poorly, to do context-aware unicode blockchars
   ie have a left-half-block if pixel to left is opaque but right isn't
 * Probably still more cool arguments/switches I haven't thought up
 * needs some kind of tests... oh boy
"""


import argparse
from PIL import Image
from sys import exit
from os import get_terminal_size


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
    Takes in a transparency value and maps it to a character. The idea
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


def get_char_from_brightness(r, g, b):
    """
    Takes in a rgb values and maps their total brightness to a character.
    Sometimes this is cuter than using alpha (in small outputs for example)
    :param a: int, min 0, max 255, alpha value of a pixel
    :return: character fitting alpha value
    """
    brightness = r + g + b  # max. 765
    for i, interval in enumerate(INTERVALS):
        if brightness >= interval*3:
            return CHARS[i]
    return '🚩'  #UNICODE_ONLY


def main(img_path, max_height=None, max_width=None, char_by_brightness=False):
    """
    get terminal dimensions,
    generate output,
    print output to terminal
    :param img_path: str, path to image file
    :param dims: tuple of ints || None, maximum number of output cells.
        None defaults to terminal size.
    """
    if DEBUG:
        print(f'Begin processing {img_path}')
    # assume a terminal character is about twice as tall as it is wide
    if max_height == None:
        max_height = get_terminal_size().lines - 1  # -1 accounts for prompt line
    if max_width == None:
        max_width = get_terminal_size().columns // 2
    im = Image.open(img_path).convert("RGBA")  # TODO error handling af
    if DEBUG:
        print(f'Original dims h:{im.height}, w:{im.width}\n'
              f'Maximum dims h:{max_height}, w:{max_width}')
    im = resize_image_to_fit(im, max_height, max_width)
    if DEBUG:
        print(f'Resized dims h:{im.height}, w:{im.width}')

    output = []
    for j in range(im.size[1]):
        for i in range(im.size[0]):  # one iteration for each char in output
            pix = im.getpixel((i, j))
            r = pix[0]
            g = pix[1]
            b = pix[2]
            a = pix[3]
            if char_by_brightness:
                char = get_char_from_brightness(r, g, b)
                if a < 20:  # prevent weird artifacting from resize...
                    char = ' '
            else:
                char = get_char_from_alpha(a)

            output += f"\033[38;2;{r};{g};{b}m{char}" * 2 + "\033[38;2;255;255;255m"
        output += "\n"  # line break at end of each row

    for c in output:
        print(c, end="")

    if DEBUG:
        print(f'Finished processing {img_path}')
    exit(0)


if __name__ == "__main__":
    """
    set up and parse args,
    interpret args,
    call main
    """
    cell_warning = 'note that a cell is roughly square, i.e. it is '\
        '2 terminal characters wide and 1 terminal character tall.'

    argparser = argparse.ArgumentParser()

    argparser.add_argument('-d', '--debug', action='store_true',
        required=False, default=False,
        help='reduce output dims, print helpful info')

    # TODO handle bad indiv. values and combinations of these
    argparser.add_argument('-H', '--max-height', action='store', type=int,
        required=False, default=None,
        help='Restrict output to this many rows at most; ' + cell_warning)

    argparser.add_argument('-W', '--max-width', action='store', type=int,
        required=False, default=None,
        help='Restrict output to this many columns at most; ' + cell_warning)

    argparser.add_argument('-b', '--char-by-brightness', action='store_true',
        required=False, default=False, help='Use brightness (instead of '
        'alpha) to determine character used to represent an input region in output.')

    argparser.add_argument('-c', '--char-offset', action='store', type=int,
        required=False, default=0, help='remove <arg> chars from high output options; '
        f'sometimes block chars are ugly so you may want to use -c 4, for example. '
        'Available chars are: {CHARS}')

    argparser.add_argument('-C', '--negative-char-offset', action='store', type=int,
        required=False, default=0, help='remove <arg> chars from low output options; '
        f'sometimes block chars are ugly so you may want to use -c 4, for example. '
        'Available chars are: {CHARS}')

    argparser.add_argument('-i', '--invert', action='store_true',
        required=False, default=False,
        help='when using -b (--char-by-brightness), invert the effect of '
            'brightness on char selection; useful for images with dark '
            'foregrounds and bright backgrounds.')

    # TODO not a bad idea but surprisingly not working?
    #argparser.add_argument('-w', '--no-whitespace', action='store_true',
        #required=False, default=False,
        #help='if this flag is set, disallow whitespace (completely transparent blocks) '
            #'in output.')

    argparser.add_argument('imageFilePath')
    args = argparser.parse_args()

    #UNICODE_ONLY
    CHARS = ['\u2588', '\u2593', '\u2592', '\u2591', '@', '#', '$', '+', '-', ' ']
    NUM_CHARS = len(CHARS)
    DEBUG = args.debug
    offset = args.char_offset
    negative_offset = args.negative_char_offset

    if offset + negative_offset >= NUM_CHARS - 1:
        print(f'error: total character offset argument must be < {NUM_CHARS-1} '
            f'to get any visible output; see `{__file__} -h`.')
        exit(1)
    CHARS = CHARS[offset:]
    if negative_offset != 0:
        CHARS = CHARS[:-1*negative_offset - 1]
        CHARS.append(' ')
    if args.invert:
        CHARS = CHARS[-1::-1]
    #if args.no_whitespace:
        #CHARS.remove(' ')
    INTERVALS = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]
    if DEBUG:
        print(f'working with these chars: {CHARS}')
    main(args.imageFilePath, args.max_height, args.max_width, args.char_by_brightness)


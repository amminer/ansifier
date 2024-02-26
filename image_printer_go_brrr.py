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
    new_height, new_width = max_height, max_width
    problem_dim = max(new_width, new_height)
    im.thumbnail((problem_dim, problem_dim), RESIZE_METHOD)

    while im.size[0] > max_width or im.size[1] > max_height:  # img > terminal
        problem_dim = max(new_width, new_height)
        im.thumbnail((problem_dim, problem_dim), RESIZE_METHOD)
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
    :param r: int, red value, max. 255
    :param g: int, green value, max. 255
    :param b: int, blue value, max. 255
    :return: character fitting brightness value
    """
    brightness = r + g + b  # max. 765
    for i, interval in enumerate(INTERVALS):
        if brightness >= interval*3:
            return CHARS[i]
    return CHARS[-1]  # unsure of whether this is a good idea... may mask issues
    return '🚩'  #UNICODE_ONLY


def main(img_path, max_height=None, max_width=None, char_by_brightness=False):
    """
    get terminal dimensions,
    generate output,
    print output to terminal
    :param img_path: str, path to image file
    :param max_height: int, maximum number of output rows. 1 row == 1 char.
        None defaults to terminal size.
    :param max_width: int, maximum number of output columns. 1 col == 2 chars.
        None defaults to terminal size.
    :param char_by_brightness: bool, whether to use pixel brightness to
        determine what character is used in the output to represent a given
        input region. Defaults to False; uses transparency instead.
    """
    if DEBUG:
        print(f'Begin processing {img_path}')
    # assume a terminal character is about twice as tall as it is wide
    if max_height == None:
        max_height = get_terminal_size().lines - 1  # -1 accounts for prompt
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

            output += f"\033[38;2;{r};{g};{b}m{char}" * 2\
                + "\033[38;2;255;255;255m"

        output += "\n"  # line break at end of each row

    for c in output:
        print(c, end="")
    if args.save_to_file is not None:
        if DEBUG:
            print(f'Writing output to {args.save_to_file}')
        with open(args.save_to_file, 'w') as wf:
            for c in output:
                wf.write(c)

    if DEBUG:
        print(f'Finished processing {img_path}')
    exit(0)


if __name__ == "__main__":
    """
    set up and parse args,
    interpret args,
    call main
    """
    #UNICODE_ONLY
    CHARS = ['\u2588', '\u2593', '\u2592', '\u2591',
        '@', '#', '$', '+', '-', ' ']
    NUM_CHARS = len(CHARS)
    resize_options = {  # input param: (PIL param, readable name)
        'lz': (Image.LANCZOS, 'Lanczos'),
        'l': (Image.LINEAR, 'linear'),
        'bl': (Image.BILINEAR, 'bilinear interpolation'),
        'c': (Image.CUBIC, 'cubic'),
        'bc': (Image.BICUBIC, 'bicubic interpolation'),
        'n': (Image.NEAREST, 'nearest neighbor'),
        'x': (Image.BOX, 'box'),
        'h': (Image.HAMMING, 'Hamming')
    }
    cell_warning = 'note that a cell is roughly square, i.e. it is '\
        '2 terminal characters wide and 1 terminal character tall.'

    argparser = argparse.ArgumentParser(
        description='In its most basic usage, takes an image file as input and '
        'prints a unicode representation of the image to the terminal, using '
        'ansi escapes for color and determining what character to use based '
        'on the transparency of the region of the image represented by that '
        'character. By default, the image is scaled to the maximum dimensions '
        'that will fit within the terminal calling this program.')

    # TODO handle bad indiv. values and combinations of these
    argparser.add_argument('-H', '--max-height', action='store', type=int,
        required=False, default=None,
        help='Restrict output to this many rows at most; ' + cell_warning)

    argparser.add_argument('-W', '--max-width', action='store', type=int,
        required=False, default=None,
        help='Restrict output to this many columns at most; ' + cell_warning)

    argparser.add_argument('-c', '--limit-high-chars', action='store', type=int,
        required=False, default=0, help='remove <arg> chars from high (opaque) '
        f'output options; Available chars are: {CHARS}')

    argparser.add_argument('-C', '--limit-low-chars', action='store',
            type=int, required=False, default=0, help='remove <arg> chars '
                f'from low (transparent) output options; preserves space char. '
                'Available chars are: {CHARS}')

    # TODO this is also a fun idea, but tricky in combination with other options
    #argparser.add_argument('-o', '--char-offset', action='store',
            #type=int, required=False, default=0, help='shift <arg> chars '
                #'higher in the array of available chars, without dropping the '
                #'space char (retains fully transparent cells). This is a WIP '
                #'and bad values are likely to break the program. '
                #f'Available chars are: {CHARS}')

    readable_resize_options = {(k, v[1]) for k, v in resize_options.items()}
    argparser.add_argument('-r', '--resize-method', action='store', type=str,
        required=False, default='lz', help='algorithm used for resampling '
            'image to desired output dimensions. Defaults to "lz", Lanczos, which '
            'tends to work best when scaling images down to normal terminal '
            f'dimensions. Options are: {readable_resize_options}')

    argparser.add_argument('-f', '--save-to-file', action='store', type=str,
        required=False, default=None, help='Write output to a file. '
            'Does not suppress terminal output. Will create or overwrite the file '
            'if needed, but will not create new directories.')

    argparser.add_argument('-b', '--char-by-brightness', action='store_true',
        required=False, default=False, help='Use brightness (instead of '
            'alpha) to determine character used to represent an input region in '
            'output.')

    argparser.add_argument('-i', '--invert', action='store_true',
        required=False, default=False,
        help='Invert the effect of transparency (or brightness when using -b '
            '(--char-by-brightness) on char selection; useful for images with '
            'dark foregrounds and bright backgrounds, for example')

    argparser.add_argument('-d', '--debug', action='store_true',
        required=False, default=False,
        help='reduce output dims, print helpful info')

    # TODO not a bad idea but surprisingly not working?
    #argparser.add_argument('-w', '--no-whitespace', action='store_true',
        #required=False, default=False,
        #help='if this flag is set, disallow whitespace '
            #'(completely transparent blocks) in output.')

    argparser.add_argument('imageFilePath')
    args = argparser.parse_args()

    DEBUG = args.debug
    RESIZE_METHOD = None
    try:
        RESIZE_METHOD = resize_options[args.resize_method][0]
    except KeyError:
        print('error: bad value passed to resize_method switch; '
            'see `{__file__} -h`.')
        exit(1)
    limit = args.limit_high_chars
    negative_limit = args.limit_low_chars
    #offset = args.char_offset

    if limit + negative_limit >= NUM_CHARS - 1:
        print(f'error: total of character limit arguments must be < {NUM_CHARS-1} '
            f'to get any visible output; see `{__file__} -h`.')
        exit(1)
    CHARS = CHARS[limit:]
    if negative_limit != 0:
        CHARS = CHARS[:-1*negative_limit - 1]
        CHARS.append(' ')
    if args.invert:
        CHARS = CHARS[-1::-1]
    #if args.no_whitespace:
        #CHARS.remove(' ')
    INTERVALS = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]
    #if offset != 0:
        #INTERVALS = [i+INTERVALS[-1 - offset] for i in INTERVALS]
        #new_offset_addition = INTERVALS[-1*offset]
        #for i, interval in enumerate(INTERVALS):
            #print(f'offset of {offset} adds {new_offset_addition} to {interval}')
            #new_interval = interval+new_offset_addition
            #if new_interval <= 255:
                #INTERVALS[i] = new_interval
    if DEBUG:
        print(f'working with these chars: {CHARS} (len {len(CHARS)})')
        print(f'working with these intervals: {INTERVALS} (len {len(INTERVALS)})')
    main(args.imageFilePath, args.max_height, args.max_width,
        args.char_by_brightness)


#!/bin/python3


import argparse

from sys import exit
from shutil import get_terminal_size

from config import CHARS, RESIZE_OPTIONS
from image_printer import ImageFilePrinter, length_after_processing


def run_cli(args=None):
    """
    Instantiates an ImageFilePrinter using argv
    calls print_text()
    may save to file if instructed
    see image_printer_go_brrr.py -h
    """
    global CHARS
    global RESIZE_OPTIONS
    NUM_CHARS = len(CHARS)

    if args is None:
        args = get_args()
    
    resize_method = None
    try:
        resize_method = RESIZE_OPTIONS[args.resize_method][0]
    except KeyError:
        print('error: bad value passed to resize_method switch; '
            f'see `{__file__} -h`.')
        exit(1)
    limit = args.limit_high_chars
    negative_limit = args.limit_low_chars
    #offset = args.char_offset

    if limit + negative_limit >= NUM_CHARS - 1:
        print(f'error: total of character limit arguments must be < '
            f'{NUM_CHARS-1} to get any visible output; see `{__file__} -h`.')
        exit(1)
    CHARS = CHARS[limit:]
    if negative_limit != 0:
        CHARS = CHARS[:-1*negative_limit - 1]
        CHARS.append(' ')
    if args.invert:
        CHARS = CHARS[-1::-1]
    #if args.no_whitespace:
        #CHARS.remove(' ')
    #INTERVALS = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]
    #if offset != 0:
        #INTERVALS = [i+INTERVALS[-1 - offset] for i in INTERVALS]
        #new_offset_addition = INTERVALS[-1*offset]
        #for i, interval in enumerate(INTERVALS):
            #print(f'offset of {offset} adds {new_offset_addition} to {interval}')
            #new_interval = interval+new_offset_addition
            #if new_interval <= 255:
                #INTERVALS[i] = new_interval
    #main(args.imageFilePath, args.max_height, args.max_width)

    image_printer = ImageFilePrinter(
        args.image_path,
        args.max_height,
        args.max_width,
        resize_method,
        args.char_by_brightness,
        CHARS,
        args.animate,
        args.loop_infinitely)

    sz = get_terminal_size()
    width = sz.columns
    height = sz.lines
    line_len = length_after_processing(image_printer.output.split('\n')[0])

    if args.center_horizontally and width > line_len+1:
        image_printer.output = '\n'.join(
            [' ' * ((width - line_len) // 2) + l\
            for l in image_printer.output.split('\n')][:-1])
        image_printer.output += '\n'

    num_lines = len(image_printer.output.split('\n'))
    if args.center_vertically and height > num_lines:
        difference = height - num_lines
        pad_num = difference // 2
        pad_line = ' ' * line_len + '\n'
        pad = pad_line*pad_num
        image_printer.output = pad_line + image_printer.output
        image_printer.output = pad + image_printer.output + pad

    
    if args.save_to_file:
        image_printer.save_text(args.save_to_file)

    return image_printer


def get_parser():
    cell_info_message = 'note that a cell is roughly square, i.e. it is '\
        '2 terminal characters wide and 1 terminal character tall.'
    argparser = argparse.ArgumentParser(
        description='In its most basic usage, takes an image file as input and '
        'prints a unicode representation of the image to the terminal, using '
        'ansi escapes for color and determining what character to use based '
        'on the transparency of the region of the image represented by that '
        'character. By default, the image is scaled to the maximum dimensions '
        'that will fit within the terminal calling this program.')

    argparser.add_argument('-H', '--max-height', action='store', type=int,
        required=False, default=None,
        help='Restrict output to this many rows at most; ' + cell_info_message)

    argparser.add_argument('-W', '--max-width', action='store', type=int,
        required=False, default=None,
        help='Restrict output to this many columns at most; ' + cell_info_message)

    argparser.add_argument('-c', '--limit-high-chars', action='store', type=int,
        required=False, default=0, help='remove <arg> chars from high (opaque) '
        f'output options; Available chars are: {CHARS}')

    argparser.add_argument('-C', '--limit-low-chars', action='store',
            type=int, required=False, default=0, help='remove <arg> chars '
                f'from low (transparent) output options; preserves space char. '
                'Available chars are: {CHARS}')

    # TODO this is a fun idea, but tricky in combination with other options
    #argparser.add_argument('-o', '--char-offset', action='store',
            #type=int, required=False, default=0, help='shift <arg> chars '
                #'higher in the array of available chars, without dropping the '
                #'space char (retains fully transparent cells). This is a WIP '
                #'and bad values are likely to break the program. '
                #f'Available chars are: {CHARS}')

    readable_resize_options = {(k, v[1]) for k, v in 
        RESIZE_OPTIONS.items()}
    argparser.add_argument('-r', '--resize-method', action='store', type=str,
        required=False, default='lz', help='algorithm used for resampling '
            'image to desired output dimensions. Defaults to "lz", Lanczos, '
            'which tends to work best when scaling images down to normal '
            f'terminal dimensions. Options are: {readable_resize_options}')

    argparser.add_argument('-a', '--animate', action='store',
        required=False, type=int, default=0,
        help='If the input image is animated (.gif), process all keyframes and '
            'print them with ANIMATE milliseconds of delay between frames. '
            'This option is incompatible with -f. '
            'It is advisable to set this value to some factor of your monitor\'s '
            'refresh rate to avoid your monitor catching ansifier mid-print.')

    argparser.add_argument('-f', '--save-to-file', action='store', type=str,
        required=False, default=None, help='Write output to a file. '
            'Does not suppress terminal output. Will create or overwrite the '
            'file if needed, but will not create new directories.')

    argparser.add_argument('-L', '--loop-infinitely', action='store_true',
        required=False, default=False,
        help='With -a --animage, causes the animation to loop until the '
        'program is terminated.')

    argparser.add_argument('-b', '--char-by-brightness', action='store_true',
        required=False, default=False, help='Use brightness (instead of '
            'alpha) to determine character used to represent an input region '
            'in output.')

    argparser.add_argument('-i', '--invert', action='store_true',
        required=False, default=False,
        help='Invert the effect of transparency (or brightness when using -b '
            '(--char-by-brightness) on char selection; useful for images with '
            'dark foregrounds and bright backgrounds, for example')

    argparser.add_argument('-z', '--center-horizontally', action='store_true',
        required=False, default=False,
        help='Use terminal size to center output horizontally. Only affects '
            'stdout, does not affect saved file contents if any, does not '
            'work on animated gifs')

    argparser.add_argument('-v', '--center-vertically', action='store_true',
        required=False, default=False,
        help='Use terminal size to center output vertically. Only affects '
            'stdout, does not affect saved file contents if any, does not '
            'work on animated gifs')

    # TODO not a bad idea but surprisingly not working?
    #argparser.add_argument('-w', '--no-whitespace', action='store_true',
        #required=False, default=False,
        #help='if this flag is set, disallow whitespace '
            #'(completely transparent blocks) in output.')

    argparser.add_argument('image_path')

    return argparser


def get_args():
    """ returns an argparser.args """
    argparser = get_parser()
    args = argparser.parse_args()
    return args


if __name__ == "__main__":
    try:
        image_printer = run_cli()
        image_printer.print_text()
    except Exception as e:
        print(e)
        exit(1)


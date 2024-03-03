"""
 TODO
 * Code is now reusable (except see below point), but significant refactoring is warranted
 * eliminate use of debug arg!!
 * Would be cool, but maybe scale poorly, to do context-aware unicode blockchars
   ie have a left-half-block if pixel to left is opaque but right isn't
 * Probably still more cool arguments/switches I haven't thought up...
   and some I have:
    - Add an option to output html/css instead of ansi escaped text file
 * eliminate conflicting option interactions (-a and -f, for example)
 * refine input sanitization
 * needs some kind of tests... oh boy
"""


import argparse
import pillow_avif  # not ref'd in code, but pillow uses this to support avif
from PIL import Image
from sys import exit
from os import path, get_terminal_size
from time import sleep


CHARS = ['\u2588', '\u2593', '\u2592', '\u2591',
         '@', '#', '$', '+', '-', ' ']


class Cell():

    def __init__(self, pixel, from_brightness=False,
                 chars=None):
        if chars is None:
            self.chars = CHARS
        else:
            self.chars = chars
        self.intervals = [255/len(self.chars)*i
                          for i in range(len(self.chars)-1, -1, -1)]
        self.pixel = pixel
        self.from_brightness = from_brightness
        self.char = self.get_char()
        r = self.pixel[0]
        g = self.pixel[1]
        b = self.pixel[2]
        self.color_escape = f"\033[38;2;{r};{g};{b}m" 
        self.reset_escape = "\033[38;2;255;255;255m"


    def __str__(self):
        ret = str(self.color_escape + self.char) * 2\
            + self.reset_escape  # TODO limit resets?
        return ret


    def get_char(self):
        if self.from_brightness:
            return self.get_char_from_brightness()
        else:
            return self.get_char_from_alpha()


    def get_char_from_brightness(self):
        char = None
        r = self.pixel[0]
        g = self.pixel[1]
        b = self.pixel[2]
        brightness = r + g + b  # max. 765
        for i, interval in enumerate(self.intervals):
            if brightness >= interval*3:
                char = self.chars[i]
                break

        if char is None:
            char = '🚩'  #UNICODE_ONLY

        return char


    def get_char_from_alpha(self):
        #TODO rgba check
        char = None
        a = self.pixel[3]
        for i, interval in enumerate(self.intervals):
            if a >= interval:
                char = self.chars[i]
                break

        if char is None:
            char = '🚩'  #UNICODE_ONLY
        elif a < 20:  # prevent weird artifacting from resize...
            char = ' '

        return char


class ImageFilePrinter():

    def __init__(self, image_path, max_height=None, max_width=None,
            resize_method=Image.LANCZOS, char_by_brightness=False, 
            chars=CHARS, save_to_file=None, animate=False):
        self.chars = chars
        self.intervals = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]
        self.image_path = image_path
        self.max_height = max_height
        self.max_width = max_width
        self.resize_method = resize_method
        self.char_by_brightness = char_by_brightness
        self.save_to_file = save_to_file
        self.animate = animate
        self.image_object = None
        if not path.exists(self.image_path):
            print(f'unable to find file {image_path}')
            exit(1)
        else:
            if args.debug:  # TODO find a better way to do this
                print(f'working with these chars: {self.chars} (len {len(self.chars)})')
                print(f'working with these intervals: {self.intervals} (len {len(self.intervals)})')
                if self.max_height is None or self.max_width is None:
                    print('Getting terminal dimensions')
            if self.max_height is None:
                self.max_height = get_terminal_size().lines - 1  # -1 accounts for prompt
            if self.max_width is None:
                self.max_width = get_terminal_size().columns // 2
            # assume a terminal character is about twice as tall as it is wide
            self.image_object = Image.open(image_path)  # TODO error handling af


    def print_ascii(self):
        if self.animate:
            self.print_animated()
        else:
            image = self.prepare_for_dump(self.image_object)
            if args.debug:
                print(f'dumping {image} to stdout')
            self.print_array(self.image_to_ascii_array(image))


    def print_array(self, ascii_array):
        for c in ascii_array:
            print(c, end="")


    def prepare_for_dump(self, image):
        image = image.convert('RGBA')
        if args.debug:
            print(f'before: {image.size}')
        image.thumbnail((self.max_width, self.max_height),
                self.resize_method)
        if args.debug:
            print(f'target: {(self.max_width, self.max_height)}')
            print(f'after: {image.size}')
        return image


    def print_animated(self):
        image = self.image_object
        frames = []
        print(f'Processing frames from {self.image_path}...')
        while True:
            if args.debug:
                print()
                print(f'Processing frame {image.tell()}')
            frame = self.prepare_for_dump(image)
            frames.append(self.image_to_ascii_array(frame))
            try:
                image.seek(image.tell() + 1)
            except EOFError:
                if args.debug:
                    print(f'No more frames in image')
                break
        done = False
        while not done:
            for frame in frames:
                if args.debug:
                    print(f'dumping {image} to stdout')
                self.print_array(frame)
                sleep(self.animate / 1000.0)
                if not args.loop_infinitely:
                    done = True


    def image_to_ascii_array(self, image=None):
        if image is None:
            image = self.image_object
        if args.debug:
            print(f'converting {image} to ascii array')
        ret = []
        for j in range(image.size[1]):
            for i in range(image.size[0]):
                pix = image.getpixel((i, j))
                cell = Cell(pix, self.char_by_brightness, self.chars)
                ret += str(cell)
            ret += "\n"  # line break at end of each row
        return ret


if __name__ == "__main__":
    """
    set up and parse args,
    interpret args,
    call main
    """
    #UNICODE_ONLY
    NUM_CHARS = len(CHARS)
    resize_options = {  # input param: (PIL param, readable name)
        'lz': (Image.LANCZOS, 'Lanczos'),
        'bl': (Image.BILINEAR, 'bilinear interpolation'),
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

    argparser.add_argument('-a', '--animate', action='store',
        required=False, type=int, default=0,
        help='If the input image is animated (.gif), process all keyframes and '
            'print them wiht ANIMATE milliseconds of delay between frames. '
            'This option is incompatible with -f.')

    argparser.add_argument('-f', '--save-to-file', action='store', type=str,
        required=False, default=None, help='Write output to a file. '
            'Does not suppress terminal output. Will create or overwrite the file '
            'if needed, but will not create new directories.')

    argparser.add_argument('-L', '--loop-infinitely', action='store_true',
        required=False, default=False,
        help='With -a --animage, causes the animation to loop until the program '
            'is terminated.')

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

    argparser.add_argument('image_path')
    args = argparser.parse_args()

    RESIZE_METHOD = None
    CHAR_BY_BRIGHTNESS = args.char_by_brightness
    ANIMATE = args.animate
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
    resize_method = resize_options[args.resize_method][0]

    image_printer = ImageFilePrinter(args.image_path,
        args.max_height, args.max_width, resize_method,
        args.char_by_brightness, CHARS,
        args.save_to_file, args.animate)
    image_printer.print_ascii()


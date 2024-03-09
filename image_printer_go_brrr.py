#!/bin/python3
"""
 TODO
 * Moved to Github issues/kanban - TODO add a docstring here
"""


import logging
from logging.handlers import RotatingFileHandler
import argparse
import pillow_avif  # not ref'd in code, but pillow uses this to support avif

from PIL import Image
from colorama import just_fix_windows_console
from os import path
from shutil import get_terminal_size
from sys import exit, stdout
from time import sleep


LOG_FILENAME = 'asciifier.log'
just_fix_windows_console()  # checks for windows internally
TERM_SUPPORTS_UTF8 = False
if stdout.encoding.lower() == 'utf-8':
    TERM_SUPPORTS_UTF8 = True

if TERM_SUPPORTS_UTF8:
    CHARS = ['\u2588', '\u2593', '\u2592', '\u2591',
            '@', '#', '$', '\u2022', '+', ':', '-', ' ']
else:
    CHARS = [chr(219), '@', '#', '$', '+', ':', '-', ' ']


class Cell():
    """
    The intended public interface for this class is:
    * instantiation with at least a tuple of (r, g, b, a) integers,
      each integer being between 0 and 255 inclusive.
      Cell((r,g,b,a)) -> <Cell object>
    * After instantiation, conversion to str is the main point of this class:
      str(cell) -> "@@" (but with an ansi escape for color)
    * inheritance, I guess??

    One block of output, 2 characters wide and 1 tall, representing one pixel
    in the input image (after any scaling).
    Character is determined by either alpha (transparency, default)
    or by brightness (total of RGB values).
    Currently, each character is composed of
        a foreground color escape,
        the character itself,
        and a reset escape
    """

    def __init__(self, pixel, from_brightness=False, chars=None):
        """
        :param pixel: tuple, of integers, length 4
            (red, green, blue, alpha) levels between 0 and 255 inclusive.
        :param from_brightness: bool, whether to use brightness to determine
            output glyph (defaults to False, which will use alpha)
        :param chars: list of 1-length strings, any non-zero length
            characters that will be selected from, intended to be ordered 
            from least to most visible when printed to a terminal
        """
        if chars is None:
            self.chars = CHARS
        else:
            self.chars = chars
        self.intervals = [255/len(self.chars)*i
                          for i in range(len(self.chars)-1, -1, -1)]
        self.pixel = pixel
        self.from_brightness = from_brightness
        self.char = self._get_char()
        r = self.pixel[0]
        g = self.pixel[1]
        b = self.pixel[2]
        self.color_escape = f"\033[38;2;{r};{g};{b}m" 
        self.reset_escape = "\033[38;2;255;255;255m"


    def __str__(self):
        # 2x printable character, assume term chars ~2x as tall as wide
        ret = str(self.color_escape + self.char) * 2\
            + self.reset_escape  # TODO limit resets?
        return ret


    def _get_char(self):
        if self.from_brightness:
            return self._get_char_from_brightness()
        else:
            return self._get_char_from_alpha()


    def _get_char_from_brightness(self):
        # TODO RGB check?
        char = None
        brightness = self.pixel[0] + self.pixel[1] + self.pixel[2]  # max. 765
        for i, interval in enumerate(self.intervals):
            if brightness >= interval*3:
                char = self.chars[i]
                break

        if char is None:
            char = '🚩'  #UNICODE_ONLY

        return char


    def _get_char_from_alpha(self):
        # TODO rgba check?
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
    """
    The intended public interface for this class is
    * Instantiation with at least an image path, the image to turn into text
      ImageFilePrinter('/path/to/image.png') -> <ImageFilePrinter>
    * After instantiation, calling ImageFilePrinter.save_text(path) will
      dump output to a file at path, assuming all parent directories exist
      and the file is writable/in a writable location... TODO error handling
    * After instantiation, calling ImageFilePrinter.print_text() will
      dump output to stdout.

    a couple of important pieces of state:
    * self.image_object is an artifact of when I was implementing animated
      gif support and should really be refactored out, TODO
    * self.image_to_dump holds the PIL.Image after RGBA conversion and resizing.
      This gets re-used for each frame when handling animated gifs;
      unsure of whether this will be a curse or a blessing when I go to
      implement dumping/loading animated gif frames to/from files.
      This should only be built once per image or once per frame for animations.
    * self.output holds the string to dump to stdout or file.
      It should only be built once, when either print_text or save_text
      are called. Subsequent calls to these functions reuse the built output.
    """

    def __init__(self, image_path, max_height=None, max_width=None,
            resize_method=Image.LANCZOS, char_by_brightness=False, 
            chars=CHARS, animate=0, logfile=None):
        """
        :param image_path: str, path to image to represent as text.
            supported image formats are those supported by PIL version 9
            as well as .avif.
        :param max_height: int, restrict output text to this number of rows
            defaults to calling terminal size (might break stuff? TODO).
        :param max_width: int, restrict output text to this number of columns
            defaults to calling terminal size (might break stuff? TODO).
        :param resize_method: PIL.Image.<ResamplingMethod>, see PIL version 9.
        :param char_by_brightness: bool, whether to use brightness to determine
            output glyphs (defaults to False, which will use alpha)
        :param chars: list of 1-length strings, any non-zero length
            characters that will be selected from, intended to be ordered 
            from least to most visible when printed to a terminal
        :param animate: int, truthiness determines whether to read keyframes
            from animated .gif image inputs and print each keyframe. If truthy,
            the int value is interpreted as the number of milliseconds to sleep
            between dumping each frame to stdout, not accounting for the time
            it takes to perform the output i.e. actual delay between frames
            may be longer depending on output dimensions, hardware, terminal
            emulator, etc.
        :param logfile: str, path to write log to. Currently, logs rotate
            with a max size of 10 MB and 2 backups. This is subject to change.
            Defaults to package_directory/asciifier.log.
        """
        self.chars = chars
        self.intervals = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]
        # TODO refactor validation into function(s)
        self.image_path = image_path
        if not path.exists(self.image_path):
            raise FileNotFoundError(f'unable to find file {image_path}')
        # TODO validate dims
        self.max_height = max_height
        self.max_width = max_width
        # TODO validate method
        self.resize_method = resize_method
        # TODO validate bool
        self.char_by_brightness = char_by_brightness
        # TODO validate uint
        self.animate = animate
        self.image_object = None
        self.image_to_dump = None
        self.output = None
        # TODO validate writable path
        logfile = LOG_FILENAME if logfile is None else logfile
        self.logger = self._initialize_logger(logfile)
        self.logger.debug(f'reading image file {image_path}')
        self.logger.debug(f'working with these chars: {self.chars} (len {len(self.chars)})')
        self.logger.debug(f'working with these intervals: {self.intervals} (len {len(self.intervals)})')
        if self.max_height is None or self.max_width is None:
            self.logger.debug('Getting terminal dimensions')
        if self.max_height is None:
            self.max_height = get_terminal_size().lines - 1  # -1 accounts for prompt
        if self.max_width is None:
            self.max_width = get_terminal_size().columns // 2
        # assume a terminal character is about twice as tall as it is wide
        self.image_object = Image.open(image_path)  # TODO error handling af


    def print_text(self):
        if self.animate:
            self._print_animated()
        else:
            if self.image_to_dump is None:
                self.image_to_dump = self.prepare_for_dump(self.image_object)
            self.logger.debug(f'dumping {self.image_to_dump} to stdout')
            self._dump_output_to_stdout(self._image_to_text_array(self.image_to_dump))


    def save_text(self, filepath):
        if self.animate:
            #self.save_animated()  # TODO dump and load gif frames!
            print(f'ERROR, saving animated GIF frames to file not yet implemented')
        else:
            if self.image_to_dump is None:
                self.image_to_dump = self.prepare_for_dump(self.image_object)
            if self.output is None:
                self._generate_output_str(self._image_to_text_array(self.image_to_dump))
            self.logger.debug(f'dumping {self.image_to_dump} to {filepath}')
            self._save_file(filepath)


    def _initialize_logger(self, logpath):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        log_formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s')
        log_file_handler = RotatingFileHandler(
            filename=logpath,
            maxBytes=10000000,  # 10 MB
            backupCount=2)
        log_file_handler.setFormatter(log_formatter)
        logger.addHandler(log_file_handler)
        return logger


    def _save_file(self, filepath):
        with open(filepath, 'w') as wf:
            for c in self.output:
                wf.write(c)

    def _generate_output_str(self, text_array):
        output = ''
        for c in text_array:
            output += c
        self.output = output

    def _dump_output_to_stdout(self, text_array):
        if self.animate or self.output is None:
            self._generate_output_str(text_array)
        print(self.output)


    def prepare_for_dump(self, image):
        image = image.convert('RGBA')
        self.logger.debug(f'before: {image.size}')
        image.thumbnail((self.max_width, self.max_height),
                self.resize_method)
        self.logger.debug(f'target: {(self.max_width, self.max_height)}')
        self.logger.debug(f'after: {image.size}')
        return image


    def _print_animated(self):
        image = self.image_object
        frames = []
        print(f'Processing frames from {self.image_path}...')
        while True:
            self.logger.debug(f'Processing frame {image.tell()}')
            frame = self.prepare_for_dump(image)
            frames.append(self._image_to_text_array(frame))
            try:
                image.seek(image.tell() + 1)
            except EOFError:
                self.logger.debug(f'No more frames in image')
                break
        done = False
        while not done:
            for frame in frames:
                self.logger.debug(f'dumping {image} to stdout')
                self._dump_output_to_stdout(frame)
                sleep(self.animate / 1000.0)
                if not args.loop_infinitely:
                    done = True


    def _image_to_text_array(self, image=None):
        #TODO This might be unnecessary - why not just go straight to string?
        if image is None:
            image = self.image_object
        self.logger.debug(f'converting {image} to text array')
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

    image_printer = ImageFilePrinter(
        args.image_path,
        args.max_height,
        args.max_width,
        RESIZE_METHOD,
        args.char_by_brightness,
        CHARS,
        args.animate)
    if args.debug:
        image_printer.logger.setLevel(logging.DEBUG)

    image_printer.print_text()

    if args.save_to_file:
        image_printer.save_text(args.save_to_file)


"""
Main purpose of this file is to expose class ImageFilePrinter for consumption

TODO/ideas for improvements not yet made into GitHub issues:
    * enhancement: refactor ImageFilePrinter to manage its memory better
        (only keep image file in memory while it absolutely has to be);
        as of right now, the image file stays in memory for the lifetime
        of the ImageFilePrinter object.
        This entails significant structural changes to the class!
        * This will also be an opportunity to refine reusability of instances.
           You should be able to resize the maximum dimensions, reload the image
           file/regenerate the output string, etc.
    * enhancement: add a docstring here
    * enhancement: generalize a wrapper for _validate functions to dry code out
    * enhancement: more robust tests that valid inputs work
    * enhancement: test for expected exceptions with bad inputs!
    * enhancement: add utf-8 check to AsciifierInputValidator, warn if warranted
    * feature/enhancement: option: disable validation (performance optimization)
    * feature: save and load gif frames to and from files (proprietary format?)
    * feature: allow ImageFilePrinter to reload image file
    * feature: add ability to mandate output dimensions
       (scale to different aspect ratios)
"""


import logging
from logging.handlers import RotatingFileHandler
import pillow_avif  # not ref'd in code, but pillow uses this to support avif

from PIL import Image
from colorama import just_fix_windows_console
from os import path, access, R_OK, W_OK
from shutil import get_terminal_size
from time import sleep


from .config import CHARS, LOG_FILENAME


class AsciifierInputValidator():
    """
    contains input validation functions
    shared between Cell and ImageFilePrinter classes.
    Only intended to be subclassed.
    """


    def _validate_char_list(self, chars):
        """
        Checks:
        1. chars is a list
            may raise TypeError
        2. len(chars) >=1
            may raise ValueError
        """
        error_t = None
        error_message = None

        if not isinstance(chars, list):
            error_t = TypeError
            error_message = f'chars parameter must be a list, but {__class__} '\
                'received {type(chars)}'

        elif not len(chars) >= 1:
            error_t = ValueError
            error_message = f'char list must have 1 or more element(s), '\
                'but {__class__} received {chars}'

        if error_t is not None:
            logger.error(message)
            raise TypeError(message)


    def _validate_positive_nonzero_int(self, i_to_check, message=None):
        """
        Checks
        1. i_to_check is an integer
        2. i_to_check is > 0
        May raise a ValueError if either check fails
        """
        if message is None:
            message = 'param must be an integer > 0, but {self.__class__} '\
                'received {i_to_check}'
        try:
            i_to_check = int(i_to_check)
        except ValueError as e:
            logger.error(str(e) + message)
            raise e  # TODO append message before raising

        if not i_to_check > 0:
            raise ValueError(message)

    
    def _validate_is_boolean(self, var_to_check, message=None):
        if message is None:
            message = 'parameter must be a boolean, '\
                'but {self.__class__} received {type(var_to_check)}'
        if not isinstance(var_to_check, bool):
            logger.error(message)
            raise TypeError(message)


class Cell(AsciifierInputValidator):
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
            chars = CHARS
        self._validate_char_list(chars)
        self.chars = chars
        self.intervals = [255/len(self.chars)*i
                          for i in range(len(self.chars)-1, -1, -1)]

        self._validate_pixel(pixel)
        self.pixel = pixel
        self.from_brightness = from_brightness
        self.char = self._get_char()
        r = self.pixel[0]
        g = self.pixel[1]
        b = self.pixel[2]
        self.color_escape = f"\033[38;2;{r};{g};{b}m" 
        self.reset_escape = "\033[38;2;255;255;255m"


    def __str__(self):
        # assume a terminal character is about twice as tall as it is wide
        ret = str(self.color_escape + self.char) * 2\
            + self.reset_escape  # TODO limit resets?
        return ret


    def _validate_pixel(self, pixel):
        """
        Checks:
        1. pixel is a tuple
            may raise TypeError
        2. pixel has 4 members
            may raise ValueError
        3. each member of pixel is an integer between 0 and 255
            may raise ValueError
        """
        error_t = None
        error_message = None
        if not isinstance(pixel, tuple):
            error_t = TypeError
            error_message = f'pixel parameter must be a tuple, but '\
                '{__class__} received a {type(pixel)}'
        elif not len(pixel) == 4:
            error_t = ValueError
            error_message = f'pixel parameter must have 4 members, but '\
                '{__class__} received {len(pixel)}'
        elif not all(map(lambda el: 0 <= el and el <= 255, pixel)):
            error_t = ValueError
            error_message = f'pixel parameter elements must each be an '\
                'integer >=0 and <=255, but {__class__} received {pixel}'

        if error_t is not None:
            logger.error(message)
            raise TypeError(message)


    def _get_char(self):
        if self.from_brightness:
            return self._get_char_from_brightness()
        else:
            return self._get_char_from_alpha()


    def _get_char_from_brightness(self):
        """ use sum of RGB values to determine char """
        char = None
        brightness = self.pixel[0] + self.pixel[1] + self.pixel[2]  # max. 765
        for i, interval in enumerate(self.intervals):
            if brightness >= interval*3:
                char = self.chars[i]
                break

        return char


    def _get_char_from_alpha(self):
        """ use transparency to determine char """
        char = None
        a = self.pixel[3]
        for i, interval in enumerate(self.intervals):
            if a >= interval:
                char = self.chars[i]
                break

        if a < 20:  # prevent weird artifacting from resize...
            char = ' '

        return char


class ImageFilePrinter(AsciifierInputValidator):
    """
    The intended public interface for this class is
    * Instantiation with at least an image path, the image to turn into text
      ImageFilePrinter('/path/to/image.png') -> <ImageFilePrinter>
    * After instantiation, calling ImageFilePrinter.save_text(path) will
      dump output to a file at path
    * After instantiation, calling ImageFilePrinter.print_text() will
      dump output to stdout.

    a couple of important pieces of state:
    * self.image_object may be an artifact of when I was implementing animated
      gif support, should probably be refactored out, TODO
    * self.image_to_dump holds the PIL.Image after RGBA conversion and resizing.
      This gets re-used for each frame when handling animated gifs;
      unsure of whether this will be a curse or a blessing when I go to
      implement dumping/loading animated gif frames to/from files.
      This should only be built once per image or once per frame for animations.
    * self.output holds the string to dump to stdout or file.
      It should only be built once, when either print_text or save_text
      are called. Subsequent calls to these functions reuse the built output.
    """

    # for validation
    resize_options = {  # input param: (PIL param, readable name)
        'n': (Image.NEAREST, 'nearest neighbor'),
        'lz': (Image.LANCZOS, 'Lanczos'),
        'bl': (Image.BILINEAR, 'bilinear interpolation'),
        'bc': (Image.BICUBIC, 'bicubic interpolation'),
        'x': (Image.BOX, 'box'),
        'h': (Image.HAMMING, 'Hamming')
    }


    def __init__(self, image_path, max_height=None, max_width=None,
            resize_method=Image.LANCZOS, char_by_brightness=False, 
            chars=CHARS, animate=0, loop_infinitely=False, logfile=None):
        """
        :param image_path: str, path to image to represent as text.
            supported image formats are those supported by PIL version 9
            as well as .avif.
        :param max_height: int, restrict output text to this number of rows
            defaults to calling terminal size from shutil.get_terminal_size
        :param max_width: int, restrict output text to this number of columns
            defaults to calling terminal size from shutil.get_terminal_size
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
        logfile = LOG_FILENAME if logfile is None else logfile
        self._validate_can_write_file(logfile)
        self.logger = self._initialize_logger(logfile)

        self._validate_char_list(chars)
        self.chars = chars
        self.intervals = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]

        self._validate_can_read_file(image_path)
        self.image_path = image_path

        valid_resize_methods = [val[0] for val in self.resize_options.values()]
        if resize_method not in valid_resize_methods:
            message = 'Invalid resize method: {resize_method}'
            logger.error(message)
            raise ValueError(message)
        self.resize_method = resize_method

        self._validate_is_boolean(char_by_brightness,
            'char_by_brightness must be a boolean, '
            'but {self.__class__} received {type(var_to_check)}')
        self.char_by_brightness = char_by_brightness

        if animate != 0:
            self._validate_positive_nonzero_int(animate,
                'animate parameter must be a non-negative integer, but '
                f'{__class__} received {animate}')
        self.animate = animate

        self._validate_is_boolean(loop_infinitely,
            'loop_infinitely must be a boolean, '
            'but {self.__class__} received {type(loop_infinitely)}')
        self.loop_infinitely = loop_infinitely

        self.image_object = None
        self.image_to_dump = None
        self.output = None
        self.frames = []

        self.logger.info(f'reading image file {image_path}')
        self.logger.debug(f'working with these chars: {self.chars} '
            '(len {len(self.chars)})')
        self.logger.debug(f'working with these intervals: {self.intervals} '
            '(len {len(self.intervals)})')
        self.max_height = max_height 
        self.max_width = max_width
        if self.max_height is None or self.max_width is None:
            self.logger.debug('Getting terminal dimensions')
        if self.max_height is None:
            self.max_height = get_terminal_size().lines - 1  # -1 for prompt
        if self.max_width is None:
            # assume a terminal character is about twice as tall as it is wide
            self.max_width = get_terminal_size().columns // 2
        self._validate_dimensions(self.max_height, self.max_width)
        try:
            self.image_object = Image.open(image_path)
        except Exception as e:
            logger.critical(e)
            raise e


    def print_text(self):
        """
        If self.animate is set,
        pass ALL responsibility to self._print_animated.
        Else, 
        if static output has not already been generated, generate it
        (according to self.max_width/self.max_height).
        Dump static output to stdout.
        """
        # checks for windows internally
        just_fix_windows_console()  # TODO limit this?

        if self.animate:
            self._print_animated()

        else:
            if self.output is None:
                self._generate_output_str(
                    self._prepare_for_dump(
                        self.image_object))
            self.logger.info(f'dumping {len(self.output)} chars derived from '
                f'{self.image_path} to stdout')
            print(self.output)


    def _print_animated(self):
        """
        If we haven't already generated text frames from the input .gif, do so.
            ^ TODO - thread this part! ^
        Then, print each frame to stdout in a loop,
        forever if self.loop_infinitely... TODO a duration might be a nice option?
        """
        image = self.image_object
        if not self.frames:
            self.logger.info(f'Processing frames from {self.image_path}...')
            while True:
                self.logger.debug(f'Processing frame {image.tell()}')
                image_frame = self._prepare_for_dump(image)
                # as a side effect, this will update self.output, but
                # I don't think this matters... should boil down to
                # just a few simple instructions per frame, once on load,
                # O(n)
                self.frames.append(self._generate_output_str(image_frame))
                try:
                    image.seek(image.tell() + 1)
                except EOFError:
                    self.logger.debug(f'No more frames to process from image')
                    break
        done = False
        frame_interval = self.animate / 1000.0
        self.logger.info(f'dumping animated image {self.image_path} to stdout '
            f'with {frame_interval}s between frames')
        while not done:
            # super important to minimize overhead in this for loop...
            # maybe a good idea to write this in C?
            for text_frame in self.frames:
                #self.logger.debug(f'dumping {len(text_frame)} chars derived '
                    #'from {self.image_path} to stdout')
                # note that frames seem to have inconsistent char len??
                print(text_frame)
                sleep(frame_interval)
            if not self.loop_infinitely:
                image.seek(0)
                done = True


    def save_text(self, filepath):
        """
        Validates filepath, then,
        if self.animate is set,
        pass ALL responsibility to self._save_animated,
        which is not yet implemented... so does nothing.
        Else, 
        if static output has not already been generated, generate it
        (according to self.max_width/self.max_height).
        Dump static output to filepath.
        """
        self._validate_can_write_file(filepath)
        if self.animate:
            #self.save_animated()  # TODO dump and load gif frames!
            self.logger.error(
                f'Saving animated GIF frames to file not yet supported')
        else:
            if self.output is None:
                self._generate_output_str(
                    self._prepare_for_dump(
                        self.image_object))
            self.logger.info(f'dumping {len(self.output)} chars derived from '
                f'{self.image_path} to {filepath}')
            self._save_file(filepath)


    def _save_file(self, filepath):
        """
        dumps self.output to filepath.
        filepath assumed to have been validated in init,
        self.output assumed to have been generated before call
        """
        with open(filepath, 'w') as wf:
            for c in self.output:
                wf.write(c)


    def _initialize_logger(self, logpath):
        """
        By default,
        logs to file at logpath with severity INFO or greater,
        logs to stdout with severity ERROR or greater.
        logpath was validated in init.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        log_formatter = logging.Formatter(
            '%(asctime)s;%(levelname)s;%(message)s')

        log_file_handler = RotatingFileHandler(
            filename=logpath,
            maxBytes=10000000,  # 10 MB
            backupCount=2)
        log_file_handler.setFormatter(log_formatter)

        log_stdout_handler = logging.StreamHandler()
        log_stdout_handler.setLevel(logging.ERROR)
        log_stdout_handler.setFormatter(log_formatter)

        logger.addHandler(log_file_handler)
        logger.addHandler(log_stdout_handler)

        return logger


    def _prepare_for_dump(self, image):
        """
        converts a PIL.Image to RGBA and resizes it according to
        self.max_width and self.max_height.
        Returns the modified Image object.
        """
        image = image.convert('RGBA')
        self.logger.debug(f'before: {image.size}')
        image.thumbnail((self.max_width, self.max_height),
                self.resize_method)
        self.logger.debug(f'target: {(self.max_width, self.max_height)}')
        self.logger.debug(f'after: {image.size}')
        return image


    def _generate_output_str(self, image):
        """
        Intent is that this should be the ONLY place self.output is assigned to.
        Call this when you need to dump output chars, but self.output is None;
        Only convert Image objects (incl. frames) to strings once if possible
        for the lifetime of the ImageFilePrinter.
        Also returns the output string in order to allow frame caching for
        animations.
        """
        self.logger.debug(f'converting {image} to ansi-escaped string')
        output = ''
        for j in range(image.size[1]):
            for i in range(image.size[0]):
                pix = image.getpixel((i, j))
                cell = Cell(pix, self.char_by_brightness, self.chars)
                output += str(cell)
            output += '\n'

        self.output = output
        return output


    def _validate_can_read_file(self, filepath):
        """
        checks three conditions:
        1. filepath exists
            may raise a FileNotFoundError
        2. filepath is not a directory (this should mean it's a file right?)
            may raise a IsADirectoryError
        3. filepath is readable (TODO this is redundant right?)
            may raise a PermissionError
        """
        error_t = None
        error_message = None
        try:
            filepath = path.abspath(filepath)
        except TypeError as e:
            self.logger.error(e)
            raise e

        if not (path.exists(filepath)):
            error_t = FileNotFoundError
            error_message = f'Unable to read file {filepath}: does not exist '\
                '(or is behind a privileged directory)'
        elif path.isdir(filepath):
            error_t = IsADirectoryError
            error_message = f'Unable to read file {filepath}: '\
                f'that\'s a directory, not a file'
        elif not access(filepath, R_OK):
            error_t = PermissionError
            error_message = f'Unable to read file {filepath}: '\
                'insufficient permissions'

        if error_t is not None:
            self.logger.error(error_message)
            raise error_t(error_message)


    def _validate_can_write_file(self, filepath):
        """
        checks three conditions:
        1. filepath's parent directory exists
            may raise FileNotFoundError
        2. filepath is not a directory (this should mean it's a file right?)
            may raise IsADirectoryError
        3. filepath's parent directory is writable
            may raise PermissionError
        """
        error_t = None
        error_message = None
        try:
            filepath = path.abspath(filepath)
        except TypeError as e:
            self.logger.error(e)
            raise e
        parent_dir = path.dirname(filepath)

        if not (path.exists(parent_dir)):
            error_t = FileNotFoundError
            error_message = f'Unable to write to {filepath}: {parent_dir} '\
                'does not exist (or is behind a privileged directory)'
        elif path.isdir(filepath):
            error_t = IsADirectoryError
            error_message = f'Unable to write to file {filepath}: '\
                f'that\'s a directory, not a file'
        elif not access(parent_dir, W_OK):
            error_t = PermissionError
            error_message = f'Unable to write to file {filepath}: '\
                'insufficient permissions'

        if error_t is not None:
            self.logger.error(error_message)
            raise error_t(error_message)


    def _validate_dimensions(self, max_height, max_width):
        """
        For each dimension, checks:
        1. dimension is an integer
        2. dimension is > 0
        May raise a ValueError if either check fails
        """
        for dim in (max_height, max_width):
            self._validate_positive_nonzero_int(dim, 'requested dimension must '
                'be an integer > 0, but {__class__} received {dim}')


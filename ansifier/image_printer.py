"""
Main purpose of this file is to expose class ImageFilePrinter for consumption

TODO/ideas for improvements not yet made into GitHub issues:
    * ENHANCEMENT: Minimize output chars; only change color when you need to
    * enhancement: add a docstring here
    * enhancement: generalize a wrapper for _validate functions to dry code out
    * enhancement: more robust tests that valid inputs work
    * enhancement: test for expected exceptions with bad inputs!
    * enhancement: add utf-8 check to ansifier, warn if warranted
    * feature/enhancement: option: disable validation (performance optimization)
    * feature: save and load gif frames to and from files (proprietary format?)
    * feature: allow ImageFilePrinter to reload image file
    * feature: add ability to mandate output dimensions
       (scale to different aspect ratios)
"""


import logging
from logging.handlers import RotatingFileHandler
import re
import signal
import sys

from PIL import Image
from colorama import just_fix_windows_console
from os import path, access, R_OK, W_OK
from shutil import get_terminal_size
from time import sleep


from config import CHARS, LOG_FILENAME, RESIZE_OPTIONS, LOG_LEVEL


# A couple of useful functions for hacking up ImageFilePrinter.output
#  post-generation

def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def length_after_processing(text):
    processed_text = remove_ansi_escape_sequences(text)
    return len(processed_text)


class AnsifierBase():
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
                f'received {type(chars)}'

        elif not len(chars) >= 1:
            error_t = ValueError
            error_message = f'char list must have 1 or more element(s), '\
                f'but {__class__} received {chars}'

        if error_t is not None:
            self.logger.error(message)
            raise TypeError(message)


    def _validate_int(self, i_to_check, minimum=0, message=None):
        """
        Checks
        1. i_to_check can be cast to integer
        2. i_to_check is > minimum
        May raise a ValueError if either check fails
        """
        if message is None:
            message = f'param must be an integer > {minimum}, but {self.__class__} '\
                f'received {i_to_check}'
        try:
            i_to_check = int(i_to_check)
        except ValueError as e:
            self.logger.error(str(e) + message)
            raise e

        if not i_to_check > minimum:
            raise ValueError(message)

    
    def _validate_is_boolean(self, var_to_check, message=None):
        if message is None:
            message = 'parameter must be a boolean, '\
                f'but {self.__class__} received {type(var_to_check)}'
        if not isinstance(var_to_check, bool):
            self.logger.error(message)
            raise TypeError(message)


class Cell(AnsifierBase):
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
        2x the character itself
    resets (\\033[38;2;255;255;255m) are to be handled by the code
    that uses the Cell
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
        #self._validate_char_list(chars)  # TODO how does this affect performance?
        self.chars = chars
        self.intervals = [255/len(self.chars)*i
                          for i in range(len(self.chars)-1, -1, -1)]
        # (how good is the interpreter at optimizing this? Does it??)

        self._validate_pixel(pixel)
        self.pixel = pixel
        self.from_brightness = from_brightness
        self.char = self._get_char()
        r = self.pixel[0]
        g = self.pixel[1]
        b = self.pixel[2]
        self.color_escape = f"\033[38;2;{r};{g};{b}m" 


    def __str__(self):
        # assume a terminal character is about twice as tall as it is wide
        if self.char == ' ':  # no need to color-escape transparent cells
            ret = self.char * 2
        else:
            ret = self.color_escape + self.char * 2
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
                f'{__class__} received a {type(pixel)}'
        elif not len(pixel) == 4:
            error_t = ValueError
            error_message = f'pixel parameter must have 4 members, but '\
                f'{__class__} received {len(pixel)}'
        elif not all(isinstance(v, int) for v in pixel) \
         and not all(map(lambda el: 0 <= el and el <= 255, pixel)):
            error_t = ValueError
            error_message = f'pixel parameter elements must each be an '\
                f'integer >=0 and <=255, but {__class__} received {pixel}'

        if error_t is not None:
            self.logger.error(message)
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


class ImageFilePrinter(AnsifierBase):
    """
    The intended public interface for this class is
    * Instantiation with at least an image path, the image to turn into text
      ImageFilePrinter('/path/to/image.png') -> <ImageFilePrinter>.
      Images are loaded into memory and converted to text output
      on object initialization.
    * Calling save_text(path) will
      dump text output to a file at path.
    * Calling print_text() will
      dump text output to stdout.
    * Calling unload_image() will unload the Image object from memory,
      but will NOT unload stored text output.
      Default behavior is to unload image after output was generated in __init__
    * Calling load_image() will load the Image object back into memory
      from the file at self.image_path
    * Calling generate_output() will always populate self.output if an image
      is loaded, and will also populate self.frames when self.animate is truthy.
      If generate_output() is called with no image loaded, nothing happens.
      

    Manipulating attributes in any other way is unsupported, at least for now.
    Dynamic changes to max_height and max_width, etc., are likely to be
    supported in the future.

    a couple of important pieces of state:
    * self.output holds the string to dump to stdout or file for static images.
      It is built when an image is loaded, on initialization or otherwise.
      ! The exception here is that animations will update this attribute as
        the object converts frames into strings to dump. Only the most recently
        converted frame is stored in this attr (NOT the most recently dumped).
    * self.frames is like self.output except it stores a list, with one element
      for each ansified frame in the last animated image that was loaded.
    """

    reset_escape = "\033[38;2;255;255;255m"

    def __eq__(self, other) :
        return self.__dict__ == other.__dict__

    def __init__(self, image_path, max_height=None, max_width=None,
            resize_method=Image.LANCZOS, char_by_brightness=False, 
            chars=CHARS, animate=0, loop_infinitely=False, logfile=None):
        """
        :param image_path: str, path to image to represent as text.
            Supported image formats are those supported by PIL version 9
        :param max_height: int, restrict output text to this number of rows
            defaults to terminal rows - 1 (to account for most prompts)
        :param max_width: int, restrict output text to this width in characters;
            One cell is two characters wide, so 1 is not a valid max_width.
            Defaults to terminal columns // 2
        :param resize_method: PIL.Image.<ResamplingMethod>, see PIL version 9;
            integer >= 0 and <= 5.
        :param char_by_brightness: bool, whether to use brightness to determine
            output glyphs (defaults to False, use alpha instead)
        :param chars: list of at least one string where each string has len 1.
            Characters that will be selected from, intended to be ordered 
            from least to most visible when printed to a terminal
        :param animate: int, truthiness determines whether to read keyframes
            from animated .gif image inputs and print each keyframe. If truthy,
            the int value is interpreted as the number of milliseconds to sleep
            between dumping each frame to stdout, not accounting for the time
            it takes to perform the output i.e. actual delay between frames
            may be longer depending on output dimensions, hardware, terminal
            emulator, etc.
            It is advisable to set this value to some factor of your monitor's
            refresh rate to avoid your monitor catching ansifier mid-print.
        """
        self.logger = None
        if logfile is None:
            logfile = path.join(path.dirname(__file__), '..', LOG_FILENAME)
        self._validate_can_write_file(logfile, log=False)
        self.logger = self._initialize_logger(logfile)

        self.image_object = None
        self.output = None
        self.output_width = None
        self.output_height = None
        self.frames = []

        type_check_message = '{} must be a {}, '\
            + f'but {self.__class__} received a' + '{}'

        self._validate_char_list(chars)
        self.chars = chars
        self.intervals = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]

        # validated in load_image
        self.image_path = image_path

        valid_resize_methods = [val[0] for val in RESIZE_OPTIONS.values()]
        valid_resize_names = [val[1] for val in RESIZE_OPTIONS.values()]
        if resize_method not in valid_resize_methods:
            message = f'Invalid resize method: {resize_method}\n'\
                f'options are {zip(valid_resize_methods, valid_resize_names)}'
            self.logger.error(message)
            raise ValueError(message)
        self.resize_method = resize_method

        if animate != 0:
            self._validate_int(animate,
                message=type_check_message.format(
                    'animate', 'non-negative integer', type(animate)))
        self.animate = animate

        self._validate_is_boolean(char_by_brightness,
            type_check_message.format(
                'char_by_brightness', 'boolean', type(char_by_brightness)))
        self.char_by_brightness = char_by_brightness

        self._validate_is_boolean(loop_infinitely,
            type_check_message.format(
                'loop_infinitely', 'boolean', type(loop_infinitely)))
        self.loop_infinitely = loop_infinitely

        self.logger.info(f'reading image file {image_path}')
        self.logger.debug(f'working with these chars: {self.chars} '
            '(len {len(self.chars)})')
        self.logger.debug(f'working with these intervals: {self.intervals} '
            '(len {len(self.intervals)})')

        if max_height is None or max_width is None:
            self.logger.debug('Getting terminal dimensions')
        if max_height is None:
            max_height = get_terminal_size().lines - 1  # -1 for prompt
        if max_width is None:
            # assume a terminal character is about twice as tall as it is wide
            max_width = get_terminal_size().columns
        self._validate_dimensions(max_height, max_width)
        self.max_height = max_height
        self.max_width = max_width // 2

        self.load_image()  # loads image into memory
        self.generate_output()  # converts self.image_object to string output
        self.logger.info('generated output with '
            f'w:{self.output_width}, h:{self.output_height}')
        self.unload_image()


    def print_text(self):
        """
        If self.animate is set,
        pass ALL responsibility to self._print_animated.
        Else, 
        Dump static output to stdout.
        """
        # checks for windows internally
        just_fix_windows_console()

        if self.animate:
            self._print_animated()

        else:
            rows = self.output.count("\n")
            self.logger.info(f'dumping {len(self.output)} chars in {rows} rows derived from '
                f'{self.image_path} to stdout')
            #sys.stdout.write(self.output)
            #sys.stdout.flush()  # TODO this might be marginally faster
            print(self.output, end='')
        print(ImageFilePrinter.reset_escape, end='')


    def _print_animated(self):
        """
        Print each frame to stdout in a loop,
        forever if self.loop_infinitely... TODO a duration might be a nice option?
        """
        self._register_sigint_handler()
        done = False
        frame_interval = self.animate / 1000.0
        self.logger.info(f'dumping {len(self.frames)} frames from '
        f'{self.image_path} to stdout with {frame_interval}s between frames')
        while not done:
            # important to minimize overhead in this for loop...
            # maybe a good idea to write this in C?
            for text_frame in self.frames:
                #self.logger.debug(f'dumping {len(text_frame)} chars derived '
                    #f'from {self.image_path} to stdout')
                #sys.stdout.write(text_frame)
                #sys.stdout.flush()  # TODO this might be marginally faster
                print(text_frame, end='')
                sleep(frame_interval)
            if not self.loop_infinitely:
                done = True


    def save_text(self, filepath):
        """
        Validates filepath, then,
        if self.animate is set,
        pass ALL responsibility to self._save_animated,
        which is not yet implemented... so does nothing.
        Else, 
        Dump static output to filepath.
        """
        self._validate_can_write_file(filepath)
        if self.animate:
            #self.save_animated()  # TODO dump and load gif frames!
            self.logger.error(
                f'Saving animated GIF frames to file not yet supported')
        else:
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


    def load_image(self):
        self._validate_can_read_file(self.image_path)
        try:
            # TODO handle DecompressionBombWarning for large images
            # this holds the file descriptor open for the lifetime of
            # the image object afaik, which seems necessary for seeks.
            self.image_object = Image.open(self.image_path, 'r')
        except Exception as e:
            self.logger.critical(e)
            raise e


    def generate_output(self):
        if self.image_object is None:
            self.logger.warning('generate_output() was called '
                'with no image loaded')
            return
        if self.animate:
            self.frames = self._convert_animation_to_frames()
        else:
            self.output = self._convert_image_to_string(
                self._prepare_for_dump(self.image_object))
        self.output_width = length_after_processing(
            self.output[:self.output.index('\n')])
        self.output_height = self.output.count('\n')


    def unload_image(self):
        """
        dellocates image object, but not the text output it generated
        """
        if self.image_object is not None:
            self.image_object.close()
        else:
            self.logger.warning('unload_image() called with no image loaded')
        self.image_object = None


    def _register_sigint_handler(self):
        """
        prints an ansi reset before doing the usual thing
        this works from source code but not from an installed wheel :|
        """
        def handler(signum, frame):
            print(ImageFilePrinter.reset_escape, end='')
            signal.default_int_handler(signum, frame)
        signal.signal(signal.SIGINT, handler)


    def _convert_animation_to_frames(self):
        self.logger.info(f'Processing frames from {self.image_path}...')
        ret = []

        while True:
            self.logger.debug(f'Processing frame {self.image_object.tell()}')
            # must be done per-seek
            image_frame = self._prepare_for_dump(self.image_object)
            # as a side effect, this will update self.output, but
            # I don't think this matters much
            ret.append(self._convert_image_to_string(image_frame))

            try:
                self.image_object.seek(self.image_object.tell() + 1)
            except EOFError:  # TODO use n frames from image_object
                self.logger.debug(f'No more frames to process from image')
                self.image_object.seek(0)
                break

        return ret


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


    def _convert_image_to_string(self, image):
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
            output += '\n'  # trailing newline per line, including final newline

        self.output = output
        self.logger.debug(f'done converting {image}')
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


    def _validate_dimensions(self, height, width):
        """
        For each dimension, checks:
        1. dimension is an integer
        2. dimension is > 0
        May raise a ValueError if either check fails
        """
        self._validate_int(height,
            message='requested height must be an integer > 0, '
                    f'but {__class__} received {height}')
        self._validate_int(width, 1,
            message='requested width must be an integer > 1, '
                    f'but {__class__} received {width}')


    def _validate_can_write_file(self, filepath, log=True):
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
            if log:
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
            if log:
                self.logger.error(error_message)
            raise error_t(error_message)


    @staticmethod
    def _initialize_logger(logpath):
        """
        By default,
        logs to file at logpath with severity INFO or greater,
        logs to stdout with severity ERROR or greater.
        logpath was validated in init.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(LOG_LEVEL)

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


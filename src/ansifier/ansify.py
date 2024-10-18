# pyright:basic
import html
import signal

from PIL import Image
from colorama import just_fix_windows_console
from shutil import get_terminal_size
from time import sleep

from .config import CHARS, RESET_ESCAPE


def _char_from_alpha(a, chars):
    char = ' '
    intervals = [255/len(CHARS)*i for i in range(len(CHARS)-1, -1, -1)]
    for i, interval in enumerate(intervals):
        if a >= interval:
            char = chars[i]
            break
    return char


def _register_sigint_handler():
    """
    prints an ansi reset before doing the usual thing
    """
    def handler(signum, frame):
        print(RESET_ESCAPE, end='')
        signal.default_int_handler(signum, frame)
    signal.signal(signal.SIGINT, handler)


## begin format bodge
# This is very inelegant, need to create an abstraction to capture all of the differences between
# output formats TODO

# functions for processing individual pixels
# :param pixel: 4-tuple of ints
# :param chars: list of str 
# :return:      str

def _pixel_to_ansi(pixel: tuple[int, ...], chars: list[str]) -> str:
    r, g, b, a = pixel
    char = _char_from_alpha(a, chars)
    color_escape = f"\033[38;2;{r};{g};{b}m" 
    reset_escape = RESET_ESCAPE
    return color_escape + char*2 + reset_escape

def _pixel_to_html(pixel: tuple[int, ...], chars: list[str]) -> str:
    r, g, b, a = pixel
    char = html.escape(_char_from_alpha(a, chars))
    if char == ' ':
        char = '&nbsp;'  # html.escape does not handle spaces...
    return f'<span style="color: rgba({r},{g},{b},{a})">{char*2}</span>' 

FORMATS = {
    'ansi-escaped': _pixel_to_ansi,
    'html/css': _pixel_to_html
}


# functions to wrap output
# :param:   None
# :return:  tuple[str, str]

FORMAT_WRAPPERS = {
    'ansi-escaped': lambda: ('', ''),
    'html/css': lambda: ('<div style="font-family: monospace; line-height: 1.2;">', '</div>')
}


# line separators per-format

FORMAT_LINEBREAKS = {
    'ansi-escaped': '\n',
    'html/css': '<br/>'
}


# what happens when an invalid format is provided

def _bad_format(output_format):
    raise ValueError(f'{output_format} is not a valid format; must be one of {list(FORMATS.keys())}')

## end format bodge


def ansify(
image_path:     str,
chars:          list[str]   = CHARS,
height:         int|None    = None,
width:          int|None    = None,
resize_method:  int         = Image.LANCZOS,  # pyright:ignore
by_intensity:   bool        = False,  # TODO
animate:        int         = 0,
loop:           bool        = False,
output_format:  str         = "ansi-escaped"
) -> str|tuple[str]:
    if height is None:
        height = get_terminal_size().lines - 1
    if width is None:
        width = get_terminal_size().columns - 1

    if animate:
        output = ''  # TODO don't forget to call _register_sigint_handler
    else:
        image = _load_image_from_file(image_path)
        _scale_image(image, height, width, resize_method)
        output = _process_image(image, output_format, chars)

    return output


def _scale_image(image, h, w, method):
    image.thumbnail((w, h), method)
    image.save('/home/meelz/temp.png')


def _load_image_from_file(image_path: str) -> Image.Image:
    """ reads a local file into a PIL Image """
    return Image.open(image_path, 'r')


def _process_image(image: Image.Image, output_format: str, chars: list[str]) -> str:
    """ takes a PIL.Image, returns a str """
    linebreak = FORMAT_LINEBREAKS.get(output_format)
    if linebreak is None:
        _bad_format(output_format)

    pixels = [
        image.getpixel((i, j))
        for j in range(image.size[1]) for i in range(image.size[0])
    ]
    cells = [
        _pixel_to_cell(pixel, output_format, chars) + (linebreak if not i % image.size[0] else '')  # pyright:ignore
        for i, pixel in enumerate(pixels)
    ]

    wrapper_function = FORMAT_WRAPPERS.get(output_format)
    if wrapper_function is None:
        _bad_format(output_format)
    prefix, suffix = wrapper_function()  # pyright:ignore

    ret = prefix + ''.join(cells) + suffix
    return ret


def _pixel_to_cell(pixel: tuple[int, ...], output_format: str, chars: list[str]) -> str:
    """ takes a (r,g,b,a) tuple, returns a pair of characters """
    conversion_function = FORMATS.get(output_format)
    if conversion_function is None:
        _bad_format(output_format)
    cell = conversion_function(pixel, chars)  # pyright:ignore
    return cell


if __name__ == '__main__':  # TODO CLI
    just_fix_windows_console()
    print(ansify('/home/meelz/Pictures/catWizard.png', output_format='ansi-escaped', height=20))

    out_path = '/home/meelz/temp.html'
    with open(out_path, 'w') as wf:
        wf.write(ansify('/home/meelz/Pictures/catWizard.png', output_format='html/css', height=60))
        print(f'wrote to {out_path}')


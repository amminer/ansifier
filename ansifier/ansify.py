"""
Main business logic;
import ansify to consume the package's functionality
"""
# pyright:basic


from filetype import guess
from PIL import Image

from .config import CHARLISTS
from .input_formats import INPUT_FORMATS
from .output_formats import OUTPUT_FORMATS


def ansify(
    input_file:     str,
    chars:          list[str]   = CHARLISTS['default'],
    height:         int         = 20,
    width:          int         = 20,
    by_intensity:   bool        = False,          # default metric is transparency; should use strategy pattern?
    input_format:   str         = '',
    output_format:  str         = 'ansi-escaped',
    animate:        bool        = True
) -> list[str]:
    """
    Takes a path to an image or video and converts it into a list of strings,
    where each string is a representation of one frame of the input media
    :param input_file:      path to image or video to convert
    :param chars:           comma-separated characters to use when converting image to text
    :params height, width:  the minimum of these values will be used to scale the image down
                            one unit of width equates to two characters because of how text is
                            typically displayed; 1 square cell of output is 2 characters wide
    :param by_intensity:    whether to use intensity (r+g+b) to pick chars; default is transparency
    :param output_format:   one of ansifiers.OUTPUT_FORMATS, depending on target display software
    :param animate:         whether to read all keyframes into output for animated inputs;
                            if False, only the first frame is converted and returned
    """
    ret = []
    if input_format == '':
        input_kind = guess(input_file)
        if input_kind is None:
            input_format = "image"
        else:
            input_format = input_kind.mime.split('/')[0]
    input_reader = INPUT_FORMATS.get(input_format)
    if input_reader is None:
        raise ValueError(
            f'{input_format} is not a valid input format; must be one of {list(INPUT_FORMATS.keys())}')

    rf = input_reader.open(input_file)
    if rf is None:
        raise(ValueError(f'unable to open {input_file}'))
    for image in input_reader.yield_frames(rf):
        ret.append(_process_frame(
            image=image,
            height=height,
            width=width,
            output_format=output_format,
            chars=chars,
            by_intensity=by_intensity))
        if not animate:
            break
    rf_close = getattr(rf, 'close', lambda:None)
    rf_close()

    return ret


def _process_frame(
    image:          Image.Image,
    height:         int,
    width:          int,
    output_format:  str,
    chars:          list[str],
    by_intensity:   bool
) -> str:
    """
    Takes a PIL Image and converts it into a string
    """
    image = image.convert('RGBA')
    image.thumbnail((width//2, height), Image.BICUBIC)  # pyright:ignore
    output_formatter = OUTPUT_FORMATS.get(output_format)
    if output_formatter is None:
        raise ValueError(
            f'{output_format} is not a valid output format; must be one of {list(OUTPUT_FORMATS.keys())}')
    ret = ''
    for j in range(image.size[1]):
        for i in range(image.size[0]):
            pixel = image.getpixel((i, j))
            char = _char_from_pixel(pixel, chars, by_intensity)  # pyright:ignore
            ret += output_formatter.char_to_cell(char, pixel[0], pixel[1], pixel[2])  # pyright:ignore
        ret += output_formatter.line_break()
    ret = output_formatter.wrap_output(ret)

    return ret


def _char_from_pixel(
    pixel:          tuple[int, int, int, int],
    chars:          list[str],
    by_intensity:   bool
) -> str:
    """ see ansify() """
    char = ' '
    intervals = [255/len(chars)*i for i in range(len(chars)-1, -1, -1)]
    metric = pixel[3]
    if by_intensity:
        metric = pixel[0] + pixel[1] + pixel[2]
    for i, interval in enumerate(intervals):
        if metric >= interval:
            char = chars[i]
            break
    return char

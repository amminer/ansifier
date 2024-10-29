"""
Main business logic;
`from ansifier import ansify` to consume the package's functionality.
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
    height:         int         = 0,
    width:          int         = 0,
    by_intensity:   bool        = False,          # strategy pattern?
    input_format:   str         = '',
    output_format:  str         = 'ansi-escaped',
    animate:        bool        = True
) -> list[str]:
    """
    Takes a path to an image or video and converts it into a list of strings,
    where each string is a representation of one frame of the input media.
    Raises a ValueError for invalid arguments.
    :param input_file:      Path to image or video to convert
    :param chars:           characters to use when converting image to text
    :params height, width:  The minimum of these values will be used to scale the image down.
                            One unit of width equates to two characters because of how text is
                            typically displayed; 1 square cell of output is 2 characters wide.
                            If only one value is provided, the other is also assigned to that value.
    :param by_intensity:    Whether to use intensity (r+g+b) to pick chars; default is transparency.
    :param input_format:    One of "image" or "video", or "" to let ansifier guess.
    :param output_format:   One of ansifiers.OUTPUT_FORMATS, depending on target display software.
    :param animate:         Whether to read all keyframes into output for animated inputs;
                            If False, only the first frame is converted and returned.
    :return:                List of frames from input file, singleton when animate == False.
    """
    ret = []
    try:
        if input_format == '':
            input_kind = guess(input_file)
            if input_kind is None:
                input_format = "image"
            else:
                input_format = input_kind.mime.split('/')[0]
        input_reader = INPUT_FORMATS.get(input_format)
    except Exception as e:
        raise ValueError(f'unable to read filetype from {input_file}, try passing input_format'
                         + '\n'+str(e))
    if input_reader is None:
        raise ValueError(
            f'{input_format} is not a valid input format; must be one of {list(INPUT_FORMATS.keys())}')

    if height == 0 and width == 0:
        height, width = 20, 20
    elif height == 0:
        height = width
    elif width == 0:
        width = height
    if height < 0 or width < 0:
        raise ValueError(f'{width} x {height} is an invalid width x height combination')

    file_error_message = f'unable to open {input_file}'
    ansifier_error_message = f'unable to process {input_file}'
    try:
        rf = input_reader.open(input_file)
    except Exception as e:
        raise(ValueError(file_error_message + '\n'+str(e)))
    if rf is None:
        raise(ValueError(file_error_message))
    try:
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
    except Exception as e:
        raise(ValueError(ansifier_error_message + '\n'+str(e)))
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
    for row in range(image.size[1]):
        for col in range(image.size[0]):
            pixel = image.getpixel((col, row))
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

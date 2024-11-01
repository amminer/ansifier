"""
Main business logic;
`from ansifier import ansify` to consume the package's functionality.
"""
# pyright:basic


import numpy as np
from filetype import guess
from PIL import Image

from .config import CHARLISTS
from .input_formats import INPUT_FORMATS
from .output_formats import OUTPUT_FORMATS, OutputFormat


def ansify(
    input_file:     str,
    chars:          list[str]|None  = None,
    height:         int             = 0,
    width:          int             = 0,
    by_intensity:   bool            = False,
    input_format:   str             = '',
    output_format:  str             = 'ansi-escaped',
    animate:        bool            = True
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
    if chars is None:
        chars = CHARLISTS['default'].copy()
    chars.reverse()  # maintains original interface while allowing for more efficient conversion...

    # determine how to read the input
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
            f'{input_format} is not a valid input format; must be one of '
            f'{list(INPUT_FORMATS.keys())}')

    # determine how to convert input images to output strings
    output_formatter = OUTPUT_FORMATS.get(output_format)
    if output_formatter is None:
        raise ValueError(
            f'{output_format} is not a valid output format; '
            f'must be one of {list(OUTPUT_FORMATS.keys())}')

    # enforce restrictions on output dimensions
    if height == 0 and width == 0:
        height, width = 20, 20
    elif height == 0:
        height = width
    elif width == 0:
        width = height
    if height < 0 or width < 0:
        raise ValueError(f'{width} x {height} is an invalid width x height combination')

    # open the input for reading
    file_error_message = f'unable to open {input_file}'
    try:
        rf = input_reader.open(input_file)
    except Exception as e:
        raise(ValueError(file_error_message + '\n'+str(e)))
    if rf is None:
        raise(ValueError(file_error_message))

    # read only as many input frames as needed, converting them to strings on the fly
    for image in input_reader.yield_frames(rf):
        image = image.convert('RGBA')
        image.thumbnail((width//2, height), Image.BICUBIC)  # pyright:ignore
        ret.append(_process_frame(
            image=image,
            chars=chars,
            by_intensity=by_intensity,
            output_formatter=output_formatter))  # pyright:ignore
        if not animate:
            break
    #print(f'output dims: {image.size}')
    #print(f'output chars: {sum((len(frame) for frame in ret))}')
    # close the input stream
    rf_close = getattr(rf, 'close', lambda:None)
    rf_close()

    return ret


def _process_frame(
    image:              Image.Image,
    chars:              list[str],
    by_intensity:       bool,
    output_formatter:   OutputFormat
) -> str:
    """
    Takes a PIL Image and converts it into a string
    """
    retlist = []  # strings are immutable; avoid churning strings

    if by_intensity:
        ceiling = 255*3
    else:
        ceiling = 255
    charmap = {i: chars[min(i // (ceiling//len(chars)), len(chars)-1)] for i in range(ceiling+1)}

    image_array = np.array(image)
    for row in image_array:
        for pixel in row:
            # If there's a way to apply the strategy pattern here without using function calls and
            # without losing the ability to optimize the output size (see conditional in
            # AnsiOutput.char_to_cell), it would be highly preferable, but I don't think there is.
            if by_intensity:
                pixel_value = pixel[0] + pixel[1] + pixel[2]
            else:
                pixel_value = pixel[3]
            char = charmap[pixel_value]
            retlist.append(
                output_formatter.char_to_cell(char, pixel[0], pixel[1], pixel[2]))  # pyright:ignore
        # it may be useful to make line_break a property instead of a method
        retlist.append(output_formatter.line_break())
    # here a prepend to a list may be needed, which is pretty slow, but if needed it's just 1x/frame...
    output_formatter.wrap_output(retlist)
    return ''.join(retlist)

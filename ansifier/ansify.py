"""
Main business logic;
import ansify to consume the package's functionality
"""
# pyright:basic


from PIL import Image

from .config import CHARLISTS
from .ansifiers import FORMATS


def ansify(
    image_path:     str,
    chars:          list[str]   = CHARLISTS['default'],
    height:         int         = 20,
    width:          int         = 20,
    by_intensity:   bool        = False,          # default metric is transparency; should use strategy pattern?
    output_format:  str         = 'ansi-escaped',
    animate:        bool        = True
) -> list[str]:
    """
    :param image_path:      path to image to convert
    :param chars:           comma-separated characters to use when converting image to text
    :params height, width:  the minimum of these values will be used to scale the image down
                            one unit of width equates to two characters because of how text is
                            typically displayed; 1 square cell of output is 2 characters wide
    :param by_intensity:    whether to use intensity (r+g+b) to pick chars; default is transparency
    :param output_format:   one of ansifiers.FORMATS, depending on target display software
    :param animate:         whether to read all keyframes into output for animated inputs;
                            if False, only the first frame is converted and returned
    """
    with Image.open(image_path, 'r') as image:
        output = []
        n_frames = getattr(image, 'n_frames', 1)
        for frame_n in range(n_frames):
            image.seek(frame_n)
            output.append(_process_image(image, height, width, output_format, chars, by_intensity))
            if not animate:
                break
    return output


def _process_image(
    image:          Image.Image,
    height:         int,
    width:          int,
    output_format:  str,
    chars:          list[str],
    by_intensity:   bool
) -> str:
    """ see ansify() """
    image = image.convert('RGBA')
    image.thumbnail((width, height), Image.BICUBIC)  # pyright:ignore
    image_processor = FORMATS.get(output_format)
    if image_processor is None:
        raise ValueError(
            f'{output_format} is not a valid format; must be one of {list(FORMATS.keys())}')
    ret = ''
    for j in range(image.size[1]):
        for i in range(image.size[0]):
            pixel = image.getpixel((i, j))
            char = _char_from_pixel(pixel, chars, by_intensity)  # pyright:ignore
            ret += image_processor.char_to_cell(char, pixel[0], pixel[1], pixel[2])  # pyright:ignore
        ret += image_processor.line_break()
    ret = image_processor.wrap_output(ret)

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

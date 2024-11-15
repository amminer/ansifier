"""
For each output format ansifier supports,
there must be a subclass of OutputFormat,
and the OUTPUT_FORMATS map at the bottom of this file must map a string to it.

An OutputFormat converts a list of PIL Images
into a list of strings
"""
# pyright: strict


from abc import ABC, abstractmethod
from html import escape


class OutputFormat(ABC):
    @staticmethod
    @abstractmethod
    def char_to_cell(char: str, r: int, g: int, b: int) -> str:
        """ output cells should display as two monospace characters. Called on every pixel. """
        pass

    @staticmethod
    @abstractmethod
    def line_break() -> str:
        """
        returns whatever string causes a line break to occur in the output format.
        """
        pass

    @staticmethod
    @abstractmethod
    def wrap_output(frame:list[str]) -> None:
        """
        Should prepend and append any necessary wrapper text to the output frame.
        Called on every frame.
        """
        pass


class Ansi16Output(OutputFormat):

    ansi_truecolor_to_4_bit = {  # uses VGA RGB
        (0, 0, 0)       : 30,  # black
        (170, 0, 0)     : 31,  # red
        (0, 170, 0)     : 32,  # green
        (170, 85, 0)    : 33,  # yellow
        (0, 0, 170)     : 34,  # blue
        (170, 0, 170)   : 35,  # magenta
        (0, 170, 170)   : 36,  # cyan
        (170, 170, 170) : 37,  # white
        (85, 85, 85)    : 90,  # grey
        (255, 85, 85)   : 91,  # bright red
        (85, 252, 85)   : 92,  # bright green
        (255, 255, 85)  : 93,  # bright yellow
        (92, 92, 252)   : 94,  # bright blue
        (255, 85, 255)  : 95,  # bright magenta
        (85, 255, 255)  : 96,  # bright cyan
        (255, 255, 255) : 97}  # bright white

    @staticmethod
    def char_to_cell(char: str, r: int, g: int, b: int) -> str:
        if char == ' ':
            return '  '
        else:
            # find the closest 4-bit color using VGA RGB values
            distances = {
                outcolor:
                   (int(r)-incolor[0])**2
                 + (int(g)-incolor[1])**2
                 + (int(b)-incolor[2])**2
                for incolor, outcolor in Ansi16Output.ansi_truecolor_to_4_bit.items()}
            min_dist = float('inf')
            final_outcolor = 0
            for outcolor, dist in distances.items():
                if dist < min_dist:
                    min_dist = dist
                    final_outcolor = outcolor
            return f'\033[1;{final_outcolor}m{char*2}'

    @staticmethod
    def line_break() -> str:
        return '\n'  # should I use ansi LF/CR here? Hmm

    @staticmethod
    def wrap_output(frame:list[str]) -> None:
        frame.append('\033[0;m')


class Ansi256Output(Ansi16Output):
    @staticmethod
    def char_to_cell(char: str, r: int, g: int, b: int) -> str:
        if char == ' ':
            return '  '
        else:
            # each channel has 6 "levels", 0-5; 255/5=51
            r, g, b = int(r/51), int(g/51), int(b/51)
            # add 16 to exclude 4-bit colors
            outcolor = 16 + (36 * r) + (6 * g) + b
            return f'\033[38;5;{outcolor}m{char*2}'


class AnsiTruecolorOutput(Ansi16Output):
    @staticmethod
    def char_to_cell(char: str, r: int, g: int, b: int) -> str:
        if char == ' ':
            return '  '
        else:
            return f'\033[38;2;{r};{g};{b}m{char*2}'


class HtmlOutput(OutputFormat):
    @staticmethod
    def char_to_cell(char: str, r: int, g: int, b: int) -> str:
        char = escape(char)
        if char == ' ':
            char = '&nbsp;'  # html.escape does not handle spaces...
            return f'<span>{char*2}</span>' 
        else:
            return f'<span style="color: rgb({r},{g},{b})">{char*2}</span>' 

    @staticmethod
    def line_break() -> str:
        return '<br/>'

    @staticmethod
    def wrap_output(frame:list[str]) -> None:
        frame.insert(0, '<div style="font-family: monospace; line-height: 1.2;">')
        frame.append('</div>')

# TODO use css to animate html frames?


OUTPUT_FORMATS = {
    'ansi-16'           : Ansi16Output,
    'ansi-256'          : Ansi256Output,
    'ansi-truecolor'    : AnsiTruecolorOutput,
    'html/css'          : HtmlOutput
}

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
        """ output cells should display as two monospace characters """
        pass

    @staticmethod
    @abstractmethod
    def line_break() -> str:
        """
        returns whatever string causes a line break to occur in the output format
        """
        pass

    @staticmethod
    @abstractmethod
    def wrap_output(frame:str) -> str:
        """
        Should prepend and append any necessary wrapper text to the output frame.
        Called on every frame.
        """
        pass


class AnsiOutput(OutputFormat):
    @staticmethod
    def char_to_cell(char: str, r: int, g: int, b: int) -> str:
        if char == ' ':
            ret = '  '
        else:
            ret = f'\033[38;2;{r};{g};{b}m{char*2}'
        return ret

    @staticmethod
    def line_break() -> str:
        return '\n'

    @staticmethod
    def wrap_output(frame:str) -> str:
        return frame + '\033[38;2;255;255;255m'


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
    def wrap_output(frame:str) -> str:
        return '<div style="font-family: monospace; line-height: 1.2;">' + frame + '</div>'


OUTPUT_FORMATS = {
    'ansi-escaped': AnsiOutput,
    'html/css': HtmlOutput
}

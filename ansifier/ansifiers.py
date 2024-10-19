"""
for each output format ansifier supports,
there must be a subclass of ImageParser,
and the FORMATS map at the bottom of this file must map a format string to it
"""
# pyright: strict


from abc import ABC, abstractmethod
from html import escape


class ImageParser(ABC):
    @staticmethod
    @abstractmethod
    def char_to_cell(char: str, r: int, g: int, b: int) -> str:
        """ output cells should display as two monospace characters """
        pass

    @staticmethod
    @abstractmethod
    def line_break() -> str:
        pass

    @staticmethod
    @abstractmethod
    def wrap_output(output:str) -> str:
        pass


class AnsiImageParser(ImageParser):
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
    def wrap_output(output:str) -> str:
        return output + '\033[38;2;255;255;255m'


class HtmlImageParser(ImageParser):
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
    def wrap_output(output:str) -> str:
        return '<div style="font-family: monospace; line-height: 1.2;">' + output + '</div>'


FORMATS = {
    'ansi-escaped': AnsiImageParser,
    'html/css': HtmlImageParser
}

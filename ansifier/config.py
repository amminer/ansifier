"""
shared data across components
"""
# pyright:basic

_BLOCK_CHARS = ['█', '▓', '▒', '░', ' ']

_NO_BLOCK_CHARS = ['#', '≡','±', '+', '÷', '-', ' ']

_CHARS = _BLOCK_CHARS[:-1] + _NO_BLOCK_CHARS

CHARLISTS = {
    'default': _CHARS,
    'blocks': _BLOCK_CHARS,
    'noblocks': _NO_BLOCK_CHARS,
}



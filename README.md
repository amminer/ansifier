<h1 align="center">🅰️🅽⚡️ℹ️🎏💈📧Ⓡ</h1>


## 📜 Table of Contents

- [About](#about)
- [Prerequisites](#prereqs)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)

## 🧐 About <a name = "about"></a>

`ansifier` is a python package which exposes a simple interface
for converting image files to utf-8 or ascii encoded strings.

At present, `ansifier` is only able to process image files (as opposed to videos).
It can format its colorful output using ANSI escapes for terminals
or HTML/CSS for web applications, so ansifier is kind of a silly name
as of version 0.0.12, but wasn't it always?

## 🛠 Prerequisites <a name = "prereqs"></a>

Python 3.8 and higher have been tested, with most extensive testing on python 3.10.
Older versions of Python 3 *may* work.

Output *should* work as intended on any modern terminal with
true color support, and *may* work on terminals without this support,
albeit with funny looking colors. I've tested on various Linux environments and Windows
10 21H2 and higher, but not on any Macs. It works in virtual consoles which don't have true
color support - at some point in the stack the RGB escapes get converted, but I don't know
where or how.

Note that `ansifier` does NOT seem to play nice with
[bpython](https://bpython-interpreter.org/),
which is a real shame because I love that program.
Other similar environments which also make use of ANSI escapes may be similarly
disagreeable to `ansifier`'s emissions. tmux is also a problem at the moment.

Also note that the CLI provides a `-m/--meofetch` flag. If you want to use this you
have to have neofetch installed and on your `PATH` so the script can get its
output from a subprocess. See the Usage section for more details on the CLI.

## 📦 Installation <a name = "installation"></a>

This package is on PyPi - my first ever! `pip install ansifier` and you should be good to go.

## 🕹️ Usage <a name="usage"></a>

In your preferred shell, running `ansifier` or `python -m ansifier` exposes a command-line interface.

Here it is in action!


https://github.com/user-attachments/assets/801ca3d9-15b5-43a5-b0cf-e53451bca7a3



The CLI takes an extensive array of arguments which are pretty thoroughly documented in the `--help` output.

```txt
usage: ansifier [-h] [-v] [-H MAX_HEIGHT] [-W MAX_WIDTH] [-c LIMIT_HIGH_CHARS]
                [-C LIMIT_LOW_CHARS] [-F OUTPUT_FORMAT] [-r RESIZE_METHOD] [-a ANIMATE]
                [-f SAVE_TO_FILE] [-L] [-b] [-i] [-z] [-V] [-m]
                [image_path]

In its most basic usage, takes an image file as input and prints a unicode representation
of the image to the terminal, using ansi escapes for color and determining what character
to use based on the transparency of the region of the image represented by that
character. By default, the image is scaled to the maximum dimensions that will fit within
the terminal calling this program.

positional arguments:
  image_path

options:
  -h, --help            show this help message and exit
  -v, --version         print version information and exit
  -H MAX_HEIGHT, --max-height MAX_HEIGHT
                        Restrict output to this many rows at most; note that a cell is
                        roughly square, i.e. it is 2 terminal characters wide and 1
                        terminal character tall.
  -W MAX_WIDTH, --max-width MAX_WIDTH
                        Restrict output to this many columns at most; note that a cell is
                        roughly square, i.e. it is 2 terminal characters wide and 1
                        terminal character tall.
  -c LIMIT_HIGH_CHARS, --limit-high-chars LIMIT_HIGH_CHARS
                        remove <arg> chars from high (opaque) output options; Available
                        chars are: ['█', '▓', '▒', '░', '@', '#', '$', '•', '+', ':',
                        '-', ' ']
  -C LIMIT_LOW_CHARS, --limit-low-chars LIMIT_LOW_CHARS
                        remove <arg> chars from low (transparent) output options;
                        preserves space char. Available chars are: ['█', '▓', '▒', '░',
                        '@', '#', '$', '•', '+', ':', '-', ' ']
  -F OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                        how to format output text - must be one of the following: ['ansi-
                        escaped', 'html/css']
  -r RESIZE_METHOD, --resize-method RESIZE_METHOD
                        algorithm used for resampling image to desired output dimensions.
                        Defaults to "lz", Lanczos, which tends to work best when scaling
                        images down to normal terminal dimensions. Options are the keys
                        of this dict: {('h', 'Hamming'), ('lz', 'Lanczos'), ('n',
                        'nearest neighbor'), ('bl', 'bilinear interpolation'), ('bc',
                        'bicubic interpolation'), ('x', 'box')}
  -a ANIMATE, --animate ANIMATE
                        If the input image is animated (.gif), process all keyframes and
                        print them with ANIMATE milliseconds of delay between frames.
                        This option is incompatible with -f. It is advisable to set this
                        value to some factor of your monitor's refresh rate to avoid your
                        monitor catching ansifier mid-print.
  -f SAVE_TO_FILE, --save-to-file SAVE_TO_FILE
                        Write output to a file. Does not suppress terminal output. Will
                        create or overwrite the file if needed, but will not create new
                        directories.
  -L, --loop-infinitely
                        With -a, causes the animation to loop until the program is
                        terminated.
  -b, --char-by-brightness
                        Use brightness (instead of alpha) to determine character used to
                        represent an input region in output.
  -i, --invert          Invert the effect of transparency (or brightness when using -b
                        (--char-by-brightness) on char selection; useful for images with
                        dark foregrounds and bright backgrounds, for example
  -z, --center-horizontally
                        Use terminal size to center output horizontally. Only affects
                        stdout, does not affect saved file contents if any
  -V, --center-vertically
                        Use terminal size to center output vertically. Only affects
                        stdout, does not affect saved file contents if any
  -m, --meofetch        meofetch takes ansifier output and interleaves it with neofetch
                        system info, with some padding. if the terminal isn't large
                        enough, neofetch lines may be trimmed from the bottom, and/or the
                        ansi image may not display. Note that the --animate option has no
                        effect here. Note that using --center-horizontally in this
                        context is discouraged. Finally, note that --max-width and --max-
                        height may only reduce the output dimensions from those found
                        based on terminal size.
```

To use `ansifier` programatically, you can `from ansifier import ImageFilePrinter`.
Take a look at the docstring of the `ImageFilePrinter` class for how the class
is intended to be used, and how you might hack it up in ways that are only somewhat intended.

The CLI takes one argument for each parameter that `ImageFilePrinter.__init__` takes,
plus a few more. The exception is the array of characters which an `ImageFilePrinter` instance
chooses from while converting an image to text - right now this is fully configurable except that
the CLI lacks an argument for it, but it's pretty high on my priority list to add this.

## 🙏 Acknowledgements  <a name = "acknowledgements"></a>

Thanks to the maintainers of:

* [Pillow](https://github.com/python-pillow/Pillow) for implementing
all those image scaling algorithms

* [colorama](https://github.com/tartley/colorama) for dealing with Windows nonsense
  so I don't have to 😄

* [pytest](https://docs.pytest.org/en/8.0.x/), my beloved

* [angr](https://github.com/angr/angr) for teaching me how to structure a python package by example
  (and, on a mostly unrelated note, for creating one of my current favorite pieces of software)

* [this cool webpage](https://stevenacoffman.github.io/homoglyphs/) that I used to generate the title of this document

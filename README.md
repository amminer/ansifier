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

HTML/CSS output uses the [rgb() CSS function](https://www.w3schools.com/cssref/func_rgb.php),
so practically any browser being run today should handle it fine.

Note that `ansifier` does NOT seem to play nice with
[bpython](https://bpython-interpreter.org/),
which is a real shame because I love that program.
Other similar environments which also make use of ANSI escapes may be similarly
disagreeable to `ansifier`'s emissions. tmux is also a problem at the moment.

## 📦 Installation <a name = "installation"></a>

This package is on PyPi - my first ever! `pip install ansifier` and you should be good to go.
You can also use `pipx` if that's your thing, it seems cool but I haven't given it a try yet so no
promises.

## 🕹️ Usage <a name="usage"></a>

In your preferred shell, running `ansifier` or `python -m ansifier` exposes a command-line interface.

Here it is in action!


TODO update this
https://github.com/user-attachments/assets/801ca3d9-15b5-43a5-b0cf-e53451bca7a3


The CLI takes an extensive array of arguments which are pretty thoroughly documented in the `--help` output.

```txt
usage: ansifier [-h] [-v] [-H HEIGHT] [-W WIDTH] [-c CHARS] [-f INPUT_FORMAT] [-F OUTPUT_FORMAT]
                [-a ANIMATE] [-L] [-i] [-I]
                [image_path]

Takes an image file as input and prints a unicode representation of the image to the terminal.

positional arguments:
  image_path

options:
  -h, --help            show this help message and exit
  -v, --version         print version information and exit
  -H HEIGHT, --height HEIGHT
                        Restrict output to this many rows. By default, restricts output to the
                        height of the calling shell's terminal, minus one to account for the
                        prompt line. Multiline prompts not yet considered.
  -W WIDTH, --width WIDTH
                        Restrict output to twice this many columns (it takes ~2 chars to represent
                        a square). By default, restricts output to the width of the calling
                        shell's terminal.
  -c CHARS, --chars CHARS
                        comma-separated sequence of characters to be chosen from when converting
                        regions of the image to text. Should be sorted from more opaque to less
                        opaque in normal usage.There are a few special values for this argument:
                        ["default": "█,▓,▒,░,#,≡,±,+,÷,-, " "blocks": "█,▓,▒,░, " "noblocks":
                        "#,≡,±,+,÷,-, " ]
  -f INPUT_FORMAT, --input-format INPUT_FORMAT
                        mimetype of file being provided as input; must be one of the following:
                        ['image', 'video']. By default, tries to guess, falling back on image.
  -F OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                        how to format output text - must be one of the following: ['ansi-escaped',
                        'html/css']. Default is ansi-escaped.
  -a ANIMATE, --animate ANIMATE
                        If the input image is animated (.gif), process all keyframes and print
                        them with ANIMATE milliseconds of delay between frames.
  -L, --loop-infinitely
                        With -a, causes the animation to loop until the program is terminated.
  -i, --char-by-intensity
                        Use intensity (instead of transparency) to determine character used to
                        represent an input region.
  -I, --invert-char-selection
                        Invert the effect of transparency (or intensity when using -i) on char
                        selection; useful for images with dark foregrounds and bright backgrounds,
                        for example.
```

To use `ansifier` programatically, you can `from ansifier import ansify`.
This function takes most of the same arguments that the CLI takes; check the docstring,
or just read the code, it's pretty concise.

## 🙏 Acknowledgements  <a name = "acknowledgements"></a>

Thanks to the maintainers of:

* [Pillow](https://github.com/python-pillow/Pillow) for implementing all those image scaling
  algorithms

* [OpenCV](https://docs.opencv.org/4.5.4/d1/dfb/intro.html) for dealing with reading video files

* [colorama](https://github.com/tartley/colorama) for dealing with Windows nonsense
  so I don't have to 😄

* [pytest](https://docs.pytest.org/en/8.0.x/), my beloved

* [this cool webpage](https://stevenacoffman.github.io/homoglyphs/) that I used to generate the title of this document

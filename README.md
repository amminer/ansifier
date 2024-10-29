<h1 align="center">🅰️🅽⚡️ℹ️🎏💈📧Ⓡ</h1>


## 📜 Table of Contents

- [About](#about)
- [Prerequisites](#prereqs)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## 🧐 About <a name = "about"></a>

`ansifier` is a python package which exposes a simple interface
for converting image files to utf-8 or ascii encoded strings.

`ansifier` is able to process both image and video files.
It can format its colorful output using ANSI escapes for terminals
or HTML/CSS for web applications, so ansifier is kind of a silly name
as of version 0.0.12, but wasn't it always?

## 🛠 Prerequisites <a name = "prereqs"></a>

In addition to pip requirements, ansifier depends on opencv to process video inputs.
If opencv binaries aren't installed, trying to process a video will fail.

Version 0.0.15 and older were tested and should work with Python 3.8 or newer.
Version 0.1.0 and newer were tested and should work with Python 3.11 or newer.
Older Python versions may still work, but no testing has been done,
and I'm not familiar enough with when exactly language features were introduced
to have an idea of how much older you can go.

For ansi-escaped output, any modern terminal emulator on any modern operating system should work.
True color support is recommended but may not be necessary.
For example, in a virtual console with more basic color support, the RGB/true color escapes seem
to get converted at some point in the stack, although I'm not sure where.
Colors may come out a little funny. Your terminal emulator also has to be reasonably performant
to get smooth animations/videos playing.

HTML/CSS output uses the [rgb() CSS function](https://www.w3schools.com/cssref/func_rgb.php),
so practically any browser being run today should handle it fine.

Note that `ansifier` does NOT seem to play nice with
[bpython](https://bpython-interpreter.org/),
which is a real shame because I love that program.
Other similar environments which also make use of ANSI escapes may find
`ansifier`'s emissions disagreeable. tmux is also a problem at the moment.

## 📦 Installation <a name = "installation"></a>

This package is on PyPi - my first ever! `pip install ansifier` and you should be good to go.
You can also use `pipx` if that's your thing, it seems cool but I haven't given it a try yet so no
promises.

## 🕹️ Usage <a name="usage"></a>

In your preferred shell, running `ansifier` or `python -m ansifier` exposes a command-line interface.

Here it is in action!


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

At the time of writing I also maintain a web frontend for this package's functionality at
[ansifier.com](https://ansifier.com/), source code [here](https://github.com/amminer/ansifier-web).
It's in very early development, so few options are available, and the way it's written is a little
funny to say the least. You can visit this site in a browser to use the graphical frontend
or send it HTTP POSTs from wherever to use it as an API; see the source README for details.

## 🕹️ Contributing <a name="contributing"></a>

If you'd like to help improve ansifier, please open an issue first. This package has transitioned
from being a learning project for me to being something I hope will be actually useful to others,
as it has been useful to me. As such, I'm happy to accept quality contributions.

## 🙏 Acknowledgements  <a name = "acknowledgements"></a>

Thanks to the maintainers of:

* [Pillow](https://github.com/python-pillow/Pillow) for dealing with reading and scaling images

* [OpenCV](https://docs.opencv.org/4.5.4/d1/dfb/intro.html) for dealing with reading video files

* [colorama](https://github.com/tartley/colorama) for dealing with Windows nonsense
  so I don't have to 😄

* [pytest](https://docs.pytest.org/en/8.0.x/), my beloved

* [this cool webpage](https://stevenacoffman.github.io/homoglyphs/) that I used to generate the title of this document

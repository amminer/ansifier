<h1 align="center">ASCIIFIER</h1>

## 📜 Table of Contents

- [About](#about)
- [Prerequisites](#prereqs)
- [Installation](#installation)
- [Authors](#authors)
- [Built Using](#built_using)
- [Acknowledgements](#acknowledgements)

## 🧐 About <a name = "about"></a>

`asciifier` is a python package which exposes a simple interface
for converting image files to utf-8 or ascii encoded strings.
At present, `asciifier` is only able to create its colorful output using ANSI escape codes,
but plans are being made to add HTML/CSS output and potentially other formats.

## 🛠 Prerequisites <a name = "prereqs"></a>

Python 3.10 and higher *should* work. Older versions of Python *may* work.
3.9 is especially likely to be okay, but extensive testing has not been done.

`asciifier`'s ANSI-escaped output *should* work as intended on any modern terminal with
true color support, and *may* work on terminals without this support,
albeit with funny looking colors.

A comprehensive list of terminal environments where `asciifier` has been observed to
be working correctly has not been compiled, but basically any common Windows 10+ or Linux
environment should be okay. No testing or usage has taken place whatsoever on Mac OSX,
to my knowledge.

Note that `asciifier` does NOT seem to play nice with
[bpython](https://bpython-interpreter.org/),
which is a real shame because I love that program.
Other similar environments which also make use of ANSI escapes may be similarly
disagreeable to `asciifier`'s emissions.

## 📦 Installation <a name = "installation"></a>

I intend to publish `asciifier` to PyPI in the near future, but for now you have to:

* clone this repository
* create and activate a virtual environment
* use pip to install the packages in requirements.txt
  * to run tests, install requirements_dev.txt instead

If you cloned the repository to somewhere on your PYTHONPATH, you should be able to use it
like so:

```py
from asciifier import ImageFilePrinter
p = ImageFilePrinter('path/to/an/image.file')
p.print_text()
p.save_file('path/to/output.file')
```

https://github.com/amminer/asciifier/assets/107884857/3ceab1fb-dbf5-44ef-9421-5e42a34cee66

You can also run the script located in the package's root, `image_printer_go_brrr.py`,
which takes a file path as its only required argument as well as many
optional arguments to modify the output or save it to a file.
The script offers a command-line flag or argument for every feature that ImageFilePrinter
takes on initialization, as well as a few extra options for added convenience.
The --help output is pretty thorough.

Note that, for every level of resource load on every different stack, there is a different
upper bound on the output size and a lower bound on the delay between frames for printing
the output derived from animated .gif files to the terminal. This bottleneck appears to
be at the terminal emulator layer. I'm currently exploring options to improve performance,
but it's possible that there's a fundamental limitation here depending on your environment.

## 👥 Authors  <a name = "authors"></a>

So far I ([@amminer](https://github.com/amminer)) am the only contributor.

## ⚙ Built Using <a name = "built_using"></a>

AKA shoutouts to my favorite tools:

* 🐍 [Python](https://www.python.org/), of course
* 🐂 GNU [Bash](https://www.gnu.org/savannah-checkouts/gnu/bash/) and
  [Coreutils](https://www.gnu.org/savannah-checkouts/gnu/coreutils)
* 📝 [Vim](https://www.vim.org/)

Running under

* 👣 [GNOME Terminal](https://help.gnome.org/users/gnome-terminal/stable/)

On

* 🐧 [Linux Mint](https://linuxmint.com/) with
* 🌿 [Cinnamon DE](https://github.com/linuxmint/Cinnamon)

## 🙏 Acknowledgements  <a name = "acknowledgements"></a>

Big thanks to the maintainers of a few very useful packages that this package depends on.
* [Pillow](https://github.com/python-pillow/Pillow) for implementing
all those image scaling algorithms
* [colorama](https://github.com/tartley/colorama) for dealing with Windows nonsense
  so I don't have to 😄
* [pytest](https://docs.pytest.org/en/8.0.x/), my beloved

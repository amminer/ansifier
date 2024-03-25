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

At present, `ansifier` is only able to process image files (as opposed to videos),
and can only create its colorful output using ANSI
escape sequences, but plans are being made to add HTML/CSS/JS output
and potentially other formats.


## 🛠 Prerequisites <a name = "prereqs"></a>

Python 3.10 and higher *should* run this fine. Older versions of Python 3 *may* work.
3.9 is especially likely to be okay, but extensive testing has not been done.

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
disagreeable to `ansifier`'s emissions.

Also note that the CLI provides a `-m/--meofetch` flag. If you want to use this you
have to have neofetch installed and on your `PATH` so the script can get its
output from a subprocess. See the Usage section for more details on the CLI.


## 📦 Installation <a name = "installation"></a>

This package is on PyPi - my first ever! `pip install ansifier` and you should be good to go.


## 🕹️ Usage <a name="usage"></a>

`python -m ansifier` exposes a command-line interface. The CLI takes an
extensive array of arguments which are pretty thoroughly documented in the --help output.

To use `ansifier` programatically, you can `from `ansifier` import ImageFilePrinter`.
Take a look at the docstring of the `ImageFilePrinter` class for how the class
is intended to be used, and how you might hack it up in ways that are only somewhat intended.

The CLI takes one argument for each parameter that `ImageFilePrinter.__init__` takes,
plus a few more. The exception is the array of characters which an `ImageFilePrinter` instance
chooses from while converting an image to text - right now this is fully configurable except that
the CLI lacks an argument for it, but it's pretty high on my priority list to add this.

Here it is in action! This video is a little out of date - forgive me, for now.
I'll update it soon to reflect the new streamlined installation and usage process
(and the new less silly naming scheme).

https://github.com/amminer/ansifier/assets/107884857/3ceab1fb-dbf5-44ef-9421-5e42a34cee66

I'll probably give this the ability to take URLs and put it in a cloud function at some point,
but for now I'm a very broke grad student and I don't want to have to worry about having a
"make me spend money" button exposed to the internet.


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

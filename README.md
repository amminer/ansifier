<h1 align="center">🅰️🅽⚡️ℹ️🎏💈📧Ⓡ</h1>


## 📜 Table of Contents

- [About](#about)
- [Prerequisites](#prereqs)
- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)
- [Built Using](#built_using)
- [Acknowledgements](#acknowledgements)


## 🧐 About <a name = "about"></a>

`ansifier` is a python package which exposes a simple interface
for converting image files to utf-8 or ascii encoded strings.
At present, `ansifier` is only able to create its colorful output using ANSI escape codes,
but plans are being made to add HTML/CSS output and potentially other formats.


## 🛠 Prerequisites <a name = "prereqs"></a>

Python 3.10 and higher *should* work. Older versions of Python 3 *may* work.
3.9 is especially likely to be okay, but extensive testing has not been done.

`ansifier`'s ANSI-escaped output *should* work as intended on any modern terminal with
true color support, and *may* work on terminals without this support,
albeit with funny looking colors. I have noticed that
my virtual consoles display the correct characters, but with unusual looking
colors, for example - it looks like somewhere in the stack the RGB escapes get
converted to a format with less colors, but I don't know where this happens.

A comprehensive list of terminal environments where `ansifier` has been observed to
be working correctly has not been compiled, but basically any common Windows 10+ or Linux
environment should be okay. No testing or usage has taken place whatsoever on Mac OSX,
to my knowledge.

Note that `ansifier` does NOT seem to play nice with
[bpython](https://bpython-interpreter.org/),
which is a real shame because I love that program.
Other similar environments which also make use of ANSI escapes may be similarly
disagreeable to `ansifier`'s emissions.

Also note that the CLI provides a `-m/--meofetch` flag. If you want to use this you
have to have neofetch installed and on your `PATH` so the script can get its
output from a subprocess. See the Usage section for more details on the CLI.


## 📦 Installation <a name = "installation"></a>

This package is on PyPi! Simply `pip install ansifier` and you should be good to go.

You're also more than welcome to clone or download the source, which includes
development environment stuff such as tests and build configuration, if that suits
your needs. The development environment assumes that you're running linux,
and that your python is python3.


## 🕹️ Usage <a name="usage"></a>

`python -m ansifier` exposes a command-line interface. The CLI takes an
extensive array of arguments which are pretty thoroughly documented in the --help output.
More detailed external documentation is in the works, but for now this should be plenty
to get anyone up and running.

To use `ansifier` programatically, you can `from `ansifier` import ImageFilePrinter`.
More detailed external documentation is in the works, but for now take a look at
the docstrings of the `ImageFilePrinter` class for a comprehensive explanation of how the class
is intended to be used, and how you might hack it up in ways that are only somewhat intended.

The CLI takes one argument for each parameter that `ImageFilePrinter.\_\_init\_\_` takes,
plus a few more. The exception is the array of characters which an `ImageFilePrinter` instance
chooses from while converting an image to text - right now this is fully configurable except that
the CLI lacks an argument for it, but it's pretty high on my priority list to add this.

Here it is in action! This video is a little out of date - forgive me, for now.
I'll update it soon to reflect the new streamlined installation and usage process
(and the new less silly naming scheme).

https://github.com/amminer/ansifier/assets/107884857/3ceab1fb-dbf5-44ef-9421-5e42a34cee66

Finally, note that for every level of resource load on every different stack, there is a different
upper bound on the output size and a lower bound on the delay between frames for printing
the output derived from animated .gif files to the terminal. Outside of these bounds, animations
will get choppy or stutter. This bottleneck appears to
be at the terminal emulator layer. I'm always exploring options to improve performance,
but it's possible that there's a fundamental limitation here depending on your environment.


## 👥 Authors  <a name = "authors"></a>

So far I ([@amminer](https://github.com/amminer)) am the only contributor.
I would love for others to take an interest in this project, but do keep in mind
that it's my baby - I've learned a lot while working on it, and that's about
all I can hope for with any project, so in that way it's been very good to me.


## ⚙ Built Using <a name = "built_using"></a>

AKA shoutouts to my favorite tools:

* 🐍 [Python](https://www.python.org/), of course
* 📝 [Vim](https://www.vim.org/)
* 🐂 GNU [Coreutils](https://www.gnu.org/savannah-checkouts/gnu/coreutils)

Running under

* 🚀 [Alacritty](https://github.com/alacritty/alacritty)

On

* 🐧 [Linux Mint](https://linuxmint.com/) with
* 🌿 [Cinnamon DE](https://github.com/linuxmint/Cinnamon)
&
* 🍥 [Debian 12](https://www.debian.org/releases/stable/releasenotes) with
* 🪟 [i3 WM](https://i3wm.org/)


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

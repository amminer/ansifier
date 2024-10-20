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
TODO cli help output
```

To use `ansifier` programatically, you can `from ansifier import ansify`.
This function takes most of the same arguments that the CLI takes; check the docstring,
or just read the code, it's pretty concise.

## 🙏 Acknowledgements  <a name = "acknowledgements"></a>

Thanks to the maintainers of:

* [Pillow](https://github.com/python-pillow/Pillow) for implementing all those image scaling
  algorithms

* [colorama](https://github.com/tartley/colorama) for dealing with Windows nonsense
  so I don't have to 😄

* [pytest](https://docs.pytest.org/en/8.0.x/), my beloved

* [this cool webpage](https://stevenacoffman.github.io/homoglyphs/) that I used to generate the title of this document

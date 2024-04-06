main:
	python -m build

test:
	python -m pytest

clean:
	-rm ./dist/*

_pip_install:
	pip install ./dist/ansifier*py3*.whl --force-reinstall

install: clean main _pip_install

careful_install: clean test main _pip_install


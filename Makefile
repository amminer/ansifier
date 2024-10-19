main:
	python -m build

clean:
	rm ./dist/*

__pip_install:
	pip install ./dist/ansifier*py3*.whl --force-reinstall

install: clean main __pip_install

example:
	python -m ansifier.cli /home/meelz/Pictures/catWizard.png -H 40

test:
	pytest


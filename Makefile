pip:
	pip install -r ./requirements.txt && pip install -r ./dev_requirements.txt

main: pip
	python -m build

clean:
	rm ./dist/*

wipe: clean
	rm -rf ./venv

__pip_install:
	pip install ./dist/ansifier*py3*.whl --force-reinstall

install: clean main __pip_install

test:
	pytest -vrP | tee ./log/most_recent_tests.log

example:
	python -m ansifier.cli ./images-examples/catSwag.png -H 40

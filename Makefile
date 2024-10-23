pip:
	pip install -r ./requirements.txt && pip install -r ./dev_requirements.txt

main: pip
	python -m build

clean:
	if ls ./dist/*; then rm ./dist/*; fi

wipe: clean
	rm -rf ./venv

__pip_install:
	pip install ./dist/ansifier*py3*.whl --force-reinstall

install: clean main __pip_install

test:
	pytest -vrP | tee ./log/most_recent_tests.log

test_installed: install
	pytest -vrP --from-installed | tee ./log/most_recent_tests.log

example:
	python -m ansifier.cli ./images-examples/catSwag.png -H 40

pip:
	pip install --root-user-action ignore -q -r ./requirements.txt && pip install --root-user-action ignore -q -r ./dev_requirements.txt

main: pip
	python -m build 1>/dev/null

clean:
	if ls ./dist/* 2>/dev/null; then rm ./dist/*; fi

wipe: clean
	rm -rf ./venv

__pip_install:
	pip install --root-user-action ignore -q ./dist/ansifier*py3*.whl --force-reinstall

install: clean main __pip_install

test:
	pytest -vrP | tee ./log/most_recent_tests.log

test_installed: install
	pytest -vrf --from-installed | tee ./log/most_recent_tests.log

test_container:
	docker build . -t ansifier-local && docker run ansifier-local;

example:
	python -m ansifier.cli ./images-examples/catSwag.png -H 40


publish:
	python -m twine upload ./dist/ansifier-*.*

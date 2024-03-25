main:
	python -m build

test:
	PYTHONPATH=./ansifier python -m pytest

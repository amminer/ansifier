#pyright:basic


import sys
import os
import pytest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PACKAGE_NAME = 'ansifier'
FILE_PATH = os.path.realpath('.')
if os.sep + PACKAGE_NAME + os.sep in FILE_PATH:
    REPO_ROOT = FILE_PATH[:FILE_PATH.index(os.sep + PACKAGE_NAME + os.sep)+len(PACKAGE_NAME)]
else:
    REPO_ROOT = FILE_PATH[:FILE_PATH.index(os.sep + PACKAGE_NAME)+len(PACKAGE_NAME)]
sys.path.append(REPO_ROOT)


def pytest_addoption(parser):
    parser.addoption(
        '--regenerate-expectations',
        action='store_true',
        default=False,
        help='generate new expected outputs for tests which check output data'
    )
    parser.addoption(
        '--from-installed',
        action='store_true',
        default=False,
        help='whether to test ansifier as an installed package instead of directly from source'
    )

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "requires_opencv: test requires OS-installed opencv")

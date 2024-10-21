#pyright:basic


import sys
import os
import pytest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="session", autouse=True)
def add_repo_root_to_sys_path():
    """
    Ensure that the repository root is in PYTHONPATH for the entire test session.
    """
    sys.path.insert(0, REPO_ROOT)

    yield

    # Optionally, clean up by removing the repo_root from sys.path after tests
    sys.path.remove(REPO_ROOT)


def pytest_addoption(parser):
    parser.addoption(
        '--regenerate-expectations',
        action='store_true',
        default='false',
        help='generate new expected outputs for tests which check output data'
    )

#pyright:basic


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
        help='whether to test ansifier as an installed package instead of directly from source; '
            'should be coupled with --import-mode=append'
    )

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "requires_opencv: test requires OS-installed opencv")

import pytest
from kaguya.cli import ArgsHandler, create_argparser


@pytest.fixture
def parser():
    parser = create_argparser()
    return parser

""" Integration tests. """
from music_qa import __version__


def test_version():
    """ Ensure that the version matches expectation. """
    assert __version__ == "0.1.0"

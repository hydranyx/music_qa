"""
Tests for the music_qa package.
"""

from music_qa import __version__


def test_version():
    """ Assert that the module version is as expected. """
    assert __version__ == "0.1.0"

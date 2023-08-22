import pytest

from automarker.marker import _flavours_match


def test__flavours_match():
    assert _flavours_match([["python"]], ["python"])
    assert not _flavours_match([["python", "pytest"]], ["python"])
    assert _flavours_match([["python", "pytest"], ["python"]], ["python"])

import pytest
from marker import flavours_match


def test_flavours_match():
    assert flavours_match([["python"]], ["python"])
    assert not flavours_match([["python", "pytest"]], ["python"])
    assert flavours_match([["python", "pytest"], ["python"]], ["python"])

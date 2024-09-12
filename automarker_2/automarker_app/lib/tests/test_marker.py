from django.test import TestCase
from automarker_app.lib.marker import _flavours_match


class TestMarker(TestCase):
    def test__flavours_match(self):
        assert _flavours_match([["python"]], ["python"])
        assert not _flavours_match([["python", "pytest"]], ["python"])
        assert _flavours_match([["python", "pytest"], ["python"]], ["python"])

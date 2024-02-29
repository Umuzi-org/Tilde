from django.test import TestCase
from automarker_app.lib.utils import AdapterCommandOutput


class TestAdapterCommandOutputCleanTagContent(TestCase):
    def test_already_clean(self):
        result = AdapterCommandOutput._clean_tag_content("hello")
        assert result == "hello"

    def test_triangle(self):
        dirty_triangle = """

       #
      ##
     ###
    ####
    """
        result = AdapterCommandOutput._clean_tag_content(dirty_triangle)
        assert result == "       #\n      ##\n     ###\n    ####"

from automarker.utils import AdapterCommandOutput


def test_already_clean():
    result = AdapterCommandOutput._clean_tag_content("hello")
    assert result == "hello"


dirty_triangle = """

   #    
  ##      
 ### 
#### 
  
"""


def test_triangle():
    result = AdapterCommandOutput._clean_tag_content(dirty_triangle)

    assert result == "   #\n  ##\n ###\n####"

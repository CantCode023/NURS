import pytest
from bs4 import BeautifulSoup
from nurs import tag_visible, text_from_html, parse_text, has_profanity
from nurs.utils.exceptions import HasProfanity
from unittest.mock import patch, Mock

def test_tag_visible():
    soup = BeautifulSoup('<p>Test</p>', 'html.parser')
    assert tag_visible(soup.p.string)
    
    soup = BeautifulSoup('<script>Test</script>', 'html.parser')
    assert not tag_visible(soup.script.string)

def test_has_profanity():
    assert has_profanity("Javascript cookie") == True
    assert not has_profanity("Clean text")

@patch('nurs.utils.text_processing.get_page_source')
def test_parse_text(mock_get_source):
    mock_get_source.return_value = """
    <html>
        <head><title>Test Title | Site</title></head>
        <body><p>Test content</p></body>
    </html>
    """
    result = parse_text("http://test.com")
    assert "Test content" in result

@patch('nurs.utils.text_processing.get_page_source')
def test_text_from_html_with_profanity(mock_get_source):
    # Need to mock better_profanity.contains_profanity to return True
    with patch('better_profanity.profanity.contains_profanity', return_value=True):
        html_content = """
        <html>
            <head><title>Bad words | Site</title></head>
            <body><p>Test content</p></body>
        </html>
        """
        with pytest.raises(HasProfanity):
            text_from_html(html_content)
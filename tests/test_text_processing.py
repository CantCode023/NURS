import pytest
from bs4.element import Comment, Tag
from bs4 import BeautifulSoup
from nurs import tag_visible, text_from_html, parse_text
import requests
from unittest.mock import Mock, patch

def test_tag_visible():
    # Test invisible elements
    soup = BeautifulSoup('<html><script>alert(1)</script></html>', 'html.parser')
    script_element = soup.find('script').string
    assert not tag_visible(script_element)

    # Test comment
    comment = Comment('test comment')
    assert not tag_visible(comment)

    # Test visible text
    soup = BeautifulSoup('<p>Hello World</p>', 'html.parser')
    visible_text = soup.find('p').string
    assert tag_visible(visible_text)

def test_text_from_html():
    # Test basic HTML
    html = """
    <html>
        <head><title>Test Title</title></head>
        <body>
            <p>Hello World</p>
            <script>console.log('test')</script>
            <style>.test{color:red;}</style>
            <!-- Comment -->
            <p>Goodbye World</p>
        </body>
    </html>
    """
    expected = "Hello World Goodbye World"
    assert text_from_html(html).strip() == expected

    # Test empty HTML
    assert text_from_html("").strip() == ""

    # Test HTML with only invisible elements
    html_invisible = """
    <html>
        <script>console.log('test')</script>
        <style>.test{color:red;}</style>
        <!-- Comment -->
    </html>
    """
    assert text_from_html(html_invisible).strip() == ""

@patch('requests.get')
def test_parse_text(mock_get):
    # Mock the requests.get response
    mock_response = Mock()
    mock_response.text = """
    <html>
        <body>
            <p>Test content</p>
        </body>
    </html>
    """
    mock_get.return_value = mock_response

    # Test with mock URL
    result = parse_text("http://example.com")
    assert result.strip() == "Test content"
    mock_get.assert_called_once_with("http://example.com")

    # Test request failure
    mock_get.side_effect = requests.exceptions.RequestException
    with pytest.raises(mock_get.side_effect):
        parse_text("http://invalid-url.com")

if __name__ == '__main__':
    pytest.main([__file__])
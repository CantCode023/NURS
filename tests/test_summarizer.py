import pytest
from nurs import Summarizer
from nurs.utils.exceptions import EmptyText, TextTooLong
from unittest.mock import Mock, patch

@pytest.fixture
def summarizer():
    return Summarizer(api_key="API_KEY_HERE")

@pytest.fixture
def sample_text():
    return """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
    exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    """

def test_summarizer_initialization():
    summarizer = Summarizer(api_key="API_KEY_HERE")
    assert isinstance(summarizer, Summarizer)
    assert hasattr(summarizer, 'api_key')

def test_summarize_with_empty_text(summarizer):
    with pytest.raises(EmptyText):
        summarizer.summarize("")

def test_summarize_with_long_text(summarizer, sample_text):
    with pytest.raises(TextTooLong):
        summarizer.summarize(sample_text*10000)

@patch('google.generativeai.GenerativeModel')
def test_successful_summarization(mock_generative_model, summarizer, sample_text):
    mock_response = Mock()
    mock_response.text = {
        "summarize": "This article talks about lorem ipsum...",
        "review": "What I learned from the article is..."
    }
    
    mock_chat = Mock()
    mock_chat.send_message.return_value = mock_response
    
    mock_model = Mock()
    mock_model.start_chat.return_value = mock_chat
    mock_generative_model.return_value = mock_model
    
    result = summarizer.summarize(sample_text)
    assert isinstance(result, dict)
    assert "summarize" in result
    assert "review" in result

@patch('google.generativeai.GenerativeModel')
def test_api_error_handling(mock_generative_model, summarizer, sample_text):
    mock_model = Mock()
    mock_model.start_chat.side_effect = Exception("API Error")
    mock_generative_model.return_value = mock_model
    
    with pytest.raises(Exception):
        summarizer.summarize(sample_text)
import pytest
from unittest.mock import patch, Mock
from nurs import Summarizer
from nurs.utils.exceptions import EmptyText

@pytest.fixture
def summarizer():
    return Summarizer("test_api_key")

@patch('google.generativeai.GenerativeModel')
def test_summarize(mock_model, summarizer):
    mock_response = Mock()
    mock_response.text = '{"summarize": "test summary", "review": "test review"}'
    
    mock_chat = Mock()
    mock_chat.send_message.return_value = mock_response
    
    mock_model_instance = Mock()
    mock_model_instance.start_chat.return_value = mock_chat
    mock_model.return_value = mock_model_instance
    
    result = summarizer.summarize("test text")
    assert result == mock_response.text
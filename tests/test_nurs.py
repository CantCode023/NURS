import pytest
from unittest.mock import patch, Mock
from nurs import NURS

@pytest.fixture
def nurs():
    return NURS("test_gemini_key", "test_bearer")

def test_nurs_initialization(nurs):
    assert nurs.gemini_api_key == "test_gemini_key"
    assert nurs.bearer == "test_bearer"
    assert nurs.API_ENDPOINT == "https://ains-api.moe.gov.my/api"
    
@patch('requests.request')
@patch('requests.options')
def test_request_api(mock_options, mock_request, nurs):
    mock_request.return_value.json.return_value = {"data": "test"}
    
    result = nurs._request_api("/test")
    
    mock_options.assert_called_once()
    mock_request.assert_called_once()
    assert result == {"data": "test"}

@patch('nurs.NURS._request_api')
def test_get_id(mock_request_api, nurs):
    mock_request_api.return_value = {"id": 12345}
    
    id = nurs._get_id()
    
    mock_request_api.assert_called_once_with("/users/me?populate=*", "GET")
    assert id == 12345

@patch('nurs.NURS._request_api')
@patch('nurs.NURS._get_id')
@patch('nurs.Encryption.get_provider')
def test_upload(mock_get_provider, mock_get_id, mock_request_api, nurs):
    mock_get_id.return_value = 12345
    mock_get_provider.return_value = "encrypted_data"
    mock_request_api.return_value = {"success": True}
    
    mock_nilam = Mock()
    mock_nilam.get_provider_parameter.return_value = "test_param"
    
    result = nurs.upload(mock_nilam)
    
    assert mock_nilam.user == 12345
    assert mock_nilam.provider == "encrypted_data"
    mock_request_api.assert_called_once()
    assert result == {"success": True}
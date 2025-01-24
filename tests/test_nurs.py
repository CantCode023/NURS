import pytest
from unittest.mock import patch
import requests
from nurs import NURS, load_config, Encryption
data = load_config()["API_KEYS"]

@pytest.fixture
def nurs():
    return NURS(data["GEMINI_API_KEY"], data["jb_app_token"])

def test_nurs_initialization(nurs):
    assert nurs.gemini_api_key == data["GEMINI_API_KEY"]
    assert nurs.jb_app_token == data["jb_app_token"]
    assert nurs.API_ENDPOINT == "https://ains.gov.my/api"
    assert isinstance(nurs.encryption, Encryption)
    assert "Access-Control-Request-Headers" in nurs.headers
    assert "Access-Control-Request-Method" in nurs.headers
    
@patch('Encryption.get_bearer_authorization')
def test_nurs_update_headers(mock_get_bearer, nurs):
    mock_get_bearer.return_value = "Bearer 12345"
    headers = nurs._update_headers()
    
    assert "Access-Control-Request-Headers" not in headers
    assert "Access-Control-Request-Method" not in headers
    assert "Authorization" in headers
    
@patch('requests.get')
@patch('requests.options')
def test_nurs_request_api(mock_options, mock_response, nurs):
    mock_response.json.return_value = {"id": 12345, "emiil": "test@test.com", "name": "Test User"}
    nurs._request_api("/users/me?populate=*")
    
    mock_options.assert_called_once_with("https://ains.gov.my/api/users/me?populate=*", headers=nurs.headers)
    mock_response.assert_called_once_with("https://ains.gov.my/api/users/me?populate=*", headers=nurs._update_headers())
    
@patch('requests.get')
@patch('requests.options')
def test_nurs_get_id(mock_options, mock_response, nurs):
    mock_response.return_value = {"id": 12345, "emiil": "test@test.com", "name": "Test User"}
    id = nurs._request_api("/users/me?populate=*")
    
    assert id == 12345
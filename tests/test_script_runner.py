import pytest
import selenium
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from nurs import Encryption
from unittest.mock import Mock, patch

@pytest.fixture
def encryption():
    return Encryption()

def test_init(encryption):
    assert isinstance(encryption.chrome_options, Options)
    assert isinstance(encryption.current_dir, Path)
    assert encryption.encrypt_file.name == "encrypt.js"
    
def test_configure_chrome_options():
    chrome_options = Encryption._configure_chrome_options()
    assert '--headless' in chrome_options.arguments
    assert '--no-sandbox' in chrome_options.arguments
    assert '--disable-dev-shm-usage' in chrome_options.arguments
    assert isinstance(chrome_options, Options)
    
def test_create_temp_html(encryption):
    # Checking if file is created
    temp_html_path = encryption._create_temp_html()
    assert temp_html_path.exists()
    assert temp_html_path.suffix == '.html'
    
    # Check if file content is correct
    with open(temp_html_path) as f:
        content = f.read()
        assert 'encrypt.js' in content
        assert '<!DOCTYPE html>' in content
        
@patch("selenium.webdriver.Chrome")
def test_execute_script(mock_chrome, encryption):
    # Patching return value of execute script
    mock_driver = Mock()
    mock_driver.execute_script.return_value = "encrypted_string"
    mock_chrome.return_value = mock_driver
    
    # Runing execute_script
    result = encryption._execute_script("script")
    
    # Checking if result is correct
    assert result == "encrypted_string"
    mock_driver.execute_script.assert_called_once_with("script")
    mock_driver.get.assert_called_once()
    mock_driver.quit.assert_called_once()
    
@patch.object(Encryption, '_execute_script')
def test_get_provider(mock_execute_script, encryption):
    # Patching return value of execute script
    mock_execute_script.return_value = "encrypted_string"
    result = encryption.get_provider("nilam_data")
    
    # Checking if result is correct
    assert result == "encrypted_string"
    mock_execute_script.assert_called_once()
    
@patch.object(Encryption, '_execute_script')
def test_get_bearer_authorization(mock_execute_script, encryption):
    # Patching return value of execute script
    mock_execute_script.return_value = "bearer_token"
    result = encryption.get_bearer_authorization("data", "token")
    
    # Checking if result is correct
    assert result == "bearer_token"
    mock_execute_script.assert_called_once()
    
@patch('selenium.webdriver.Chrome')
def test_execute_script_error_handling(mock_chrome, encryption):
    # Raising Exception when execute_script is called
    mock_driver = Mock()
    mock_chrome.return_value = mock_driver
    mock_driver.execute_script.side_effect = Exception('Error')
    
    # Calling execute_script
    result = encryption._execute_script('script')
    
    # Checking if result is None to indicate error is handled
    assert result is None
    mock_driver.quit.assert_called_once()

@patch('selenium.webdriver.Chrome')
def test_temp_file_cleanup(mock_chrome, encryption):
    # Mocking chrome driver
    mock_driver = Mock()
    mock_chrome.return_value = mock_driver
    
    # Running execute_script
    encryption._execute_script('script')
    
    # Checking if temp file is deleted
    temp_html_path = encryption.current_dir / 'temp.html'
    assert not temp_html_path.exists()
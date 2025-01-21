import pytest
from pathlib import Path
import toml
from nurs import load_config
from unittest.mock import patch

@patch("toml.load")
def test_load_config(mock_toml):
    # Mock data
    mock_toml.return_value = {"a": "b"}
    
    # Test with function
    config = load_config()
    assert config == {"a": "b"}
    
    # Verify path
    mock_toml.asset_called_once()
    called_path = mock_toml.call_args[0][0]
    assert called_path.name == "config.toml"
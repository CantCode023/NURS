import pytest
import os
from nurs import load_config
from unittest.mock import patch

def test_load_config_with_env_vars():
    with patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test_key',
        'jb_app_token': 'test_token'
    }):
        config = load_config()
        assert config == {
            "API_KEYS": {
                "GEMINI_API_KEY": "test_key",
                "jb_app_token": "test_token"  
            }
        }

def test_load_config_without_env_vars():
    with patch.dict(os.environ, clear=True):
        config = load_config()
        assert config is None
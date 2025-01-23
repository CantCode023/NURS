from typing import Union
from .exceptions import EmptyText, TextTooLong

def validate_text(text: Union[str, None]) -> bool:
    """
    Validates text input for the summarizer
    
    Args:
        text: Input text to validate
        
    Returns:
        bool: True if text is valid
        
    Raises:
        EmptyText: If text is empty or None
        TextTooLong: If text exceeds maximum length
        TypeError: If text is not a string
    """
    MAX_LENGTH = 100000
    
    if not text or len(text.strip()) == 0:
        raise EmptyText("Text cannot be empty!")
        
    if not isinstance(text, str):
        raise TypeError("Text must be a string!")
    
    if len(text) > MAX_LENGTH:
        raise TextTooLong(f"Text length exceeds maximum limit of {MAX_LENGTH} characters")
        
    return True
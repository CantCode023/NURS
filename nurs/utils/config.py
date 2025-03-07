from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

def load_config() -> dict[str, dict[str, str]] | None:
    if "GEMINI_API_KEY" in os.environ:
        return {
            "API_KEYS": {
                "GEMINI_API_KEY": os.environ["GEMINI_API_KEY"],
                "jb_app_token": os.environ["jb_app_token"],
            }
        }
    return None
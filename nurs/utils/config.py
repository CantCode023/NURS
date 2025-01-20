from pathlib import Path
import toml

def load_config():
    config_path = Path(__file__).parent.parent.parent / 'config.toml'
    return toml.load(config_path)
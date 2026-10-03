import json
from pathlib import Path

ROOT = Path(__file__).parent

def load(name, fallback):
    try:
        return json.loads((ROOT / name).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return fallback.copy()

def store(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

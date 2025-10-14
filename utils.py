import json
import os

def save_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f, default=str)

def load_data(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return default
    return default

from datetime import datetime
import json
import os

state_file = 'state.json'

def load():
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            data = json.load(f)
            for key in data:
                if data[key]:
                    data[key] = datetime.fromisoformat(data[key])
            return data
    return {
        'pr': None,
        'issue': None,
        'release': None,
        'npm': None
    }

def save(data):
    save_data = {}
    for key, value in data.items():
        save_data[key] = value.isoformat() if value else None
    with open(state_file, 'w') as f:
        json.dump(save_data, f, indent=2)

last_check = load()
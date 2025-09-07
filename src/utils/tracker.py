import json
import os

tracker_file = 'tracker.json'

def load():
    if os.path.exists(tracker_file):
        with open(tracker_file, 'r') as f:
            return json.load(f)
    return {'issues': {}, 'prs': {}}

def save(data):
    with open(tracker_file, 'w') as f:
        json.dump(data, f, indent=2)

def track(item_type, number, message_id, channel_id):
    data = load()
    key = str(number)
    data[item_type][key] = {
        'message_id': message_id,
        'channel_id': channel_id,
        'reacted': False
    }
    save(data)

def markreacted(item_type, number):
    data = load()
    key = str(number)
    if key in data[item_type]:
        data[item_type][key]['reacted'] = True
        save(data)

def markunreacted(item_type, number):
    data = load()
    key = str(number)
    if key in data[item_type]:
        data[item_type][key]['reacted'] = False
        save(data)

def get(item_type, number):
    data = load()
    key = str(number)
    return data[item_type].get(key)
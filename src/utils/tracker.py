import json
import os

def loadfile(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def savefile(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def track(item_type, identifier, message_id, channel_id):
    filename = f'{item_type}.json'
    data = loadfile(filename)
    
    if item_type == 'releases':
        data[identifier] = {
            'message_id': message_id,
            'channel_id': channel_id,
            'timestamp': identifier
        }
    else:
        data[str(identifier)] = {
            'message_id': message_id,
            'channel_id': channel_id,
            'reacted': False
        }
    
    savefile(filename, data)

def markreacted(item_type, number):
    filename = f'{item_type}.json'
    data = loadfile(filename)
    key = str(number)
    if key in data:
        data[key]['reacted'] = True
        savefile(filename, data)

def markunreacted(item_type, number):
    filename = f'{item_type}.json'
    data = loadfile(filename)
    key = str(number)
    if key in data:
        data[key]['reacted'] = False
        savefile(filename, data)

def get(item_type, identifier):
    filename = f'{item_type}.json'
    data = loadfile(filename)
    key = str(identifier) if item_type != 'releases' else identifier
    return data.get(key)

def hasreleasebeensent(version):
    data = loadfile('releases.json')
    return version in data

def migrateolddata():
    if os.path.exists('tracker.json'):
        with open('tracker.json', 'r') as f:
            olddata = json.load(f)
        
        if 'issues' in olddata:
            savefile('issues.json', olddata['issues'])
        
        if 'prs' in olddata:
            savefile('prs.json', olddata['prs'])
        
        os.rename('tracker.json', 'tracker.json.backup')
        print('migrated tracker.json to separate files (backup saved as tracker.json.backup)')

migrateolddata()
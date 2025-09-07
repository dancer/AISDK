from src import config

def github():
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-SDK-Monitor-Bot'
    }
    if config.github_token:
        headers['Authorization'] = f'Bearer {config.github_token}'
    return headers
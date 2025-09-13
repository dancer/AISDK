import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
github_token = os.getenv('GITHUB_TOKEN')
owner_id = int(os.getenv('OWNER_ID', 0))
github_repo = 'vercel/ai'
npm_package = 'ai'

channels = {
    'prs': int(os.getenv('CHANNEL_PRS', 0)),
    'issues': int(os.getenv('CHANNEL_ISSUES', 0)),
    'releases': int(os.getenv('CHANNEL_RELEASES', 0)),
    'ai': int(os.getenv('CHANNEL_AI', 0))
}
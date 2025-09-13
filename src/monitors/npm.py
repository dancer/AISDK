import aiohttp
from datetime import datetime
from src import config
from src.utils import state, tracker
from src.formatters.embed import formatnpm

async def checknpm(sendwebhook, bot):
    async with aiohttp.ClientSession() as session:
        url = f'https://registry.npmjs.org/{config.npm_package}'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                latest = data['dist-tags']['latest']
                modified = data['time'][latest]
                
                if not tracker.hasreleasebeensent(latest):
                    message = await sendwebhook('releases', formatnpm(latest, data['versions'][latest]))
                    if message:
                        tracker.track('releases', latest, message.id, message.channel.id)
                
                state.last_check['npm'] = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                state.save(state.last_check)
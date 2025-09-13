import aiohttp
from datetime import datetime
from src import config
from src.utils import state
from src.utils.headers import github
from src.formatters.embed import formatpr, formatissue

async def checkprs(sendwebhook, bot):
    from src.utils import tracker, emojis
    
    async with aiohttp.ClientSession() as session:
        url = f'https://api.github.com/repos/{config.github_repo}/pulls?state=all'
        headers = github()
        
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                prs = await response.json()
                
                for pr in prs:
                    existing = tracker.get('prs', pr['number'])
                    if existing:
                        if pr['state'] == 'closed' and not existing.get('reacted', False):
                            try:
                                channel = bot.get_channel(existing['channel_id'])
                                if channel:
                                    message = await channel.fetch_message(existing['message_id'])
                                    
                                    if pr.get('merged'):
                                        emoji = bot.get_emoji(emojis.merge)
                                    else:
                                        emoji = bot.get_emoji(emojis.closed)
                                    
                                    if emoji:
                                        await message.add_reaction(emoji)
                                        tracker.markreacted('prs', pr['number'])
                            except Exception as e:
                                print(f'error adding pr reaction: {e}')
                        elif pr['state'] == 'open' and existing.get('reacted', False):
                            try:
                                channel = bot.get_channel(existing['channel_id'])
                                if channel:
                                    message = await channel.fetch_message(existing['message_id'])
                                    for emoji_id in [emojis.merge, emojis.closed]:
                                        emoji = bot.get_emoji(emoji_id)
                                        if emoji:
                                            try:
                                                await message.remove_reaction(emoji, bot.user)
                                            except:
                                                pass
                                    tracker.markunreacted('prs', pr['number'])
                                    print(f'removed reactions from pr {pr["number"]}')
                            except Exception as e:
                                print(f'error removing pr reaction: {e}')
                    
                    if state.last_check['pr']:
                        if datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00')) > state.last_check['pr']:
                            await sendwebhook('prs', formatpr(pr), 'prs', pr['number'])
                
                if prs:
                    state.last_check['pr'] = datetime.fromisoformat(prs[0]['created_at'].replace('Z', '+00:00'))
                    state.save(state.last_check)

async def checkissues(sendwebhook, bot):
    from src.utils import tracker, emojis
    
    async with aiohttp.ClientSession() as session:
        url = f'https://api.github.com/repos/{config.github_repo}/issues?state=all'
        headers = github()
        
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                issues = await response.json()
                issues = [i for i in issues if 'pull_request' not in i]
                
                for issue in issues:
                    existing = tracker.get('issues', issue['number'])
                    if existing:
                        if issue['state'] == 'closed' and not existing.get('reacted', False):
                            try:
                                channel = bot.get_channel(existing['channel_id'])
                                if channel:
                                    message = await channel.fetch_message(existing['message_id'])
                                    emoji = bot.get_emoji(emojis.fixed)
                                    if emoji:
                                        await message.add_reaction(emoji)
                                        tracker.markreacted('issues', issue['number'])
                            except:
                                pass
                        elif issue['state'] == 'open' and existing.get('reacted', False):
                            try:
                                channel = bot.get_channel(existing['channel_id'])
                                if channel:
                                    message = await channel.fetch_message(existing['message_id'])
                                    emoji = bot.get_emoji(emojis.fixed)
                                    if emoji:
                                        await message.remove_reaction(emoji, bot.user)
                                        tracker.markunreacted('issues', issue['number'])
                            except:
                                pass
                
                    if state.last_check['issue']:
                        if datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00')) > state.last_check['issue']:
                            await sendwebhook('issues', formatissue(issue), 'issues', issue['number'])
                
                if issues:
                    state.last_check['issue'] = datetime.fromisoformat(issues[0]['created_at'].replace('Z', '+00:00'))
                    state.save(state.last_check)


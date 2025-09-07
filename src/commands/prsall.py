import discord
from discord.ext import commands
import aiohttp
import asyncio
from src import config
from src.formatters.embed import formatpr
from src.utils.embed import error, success
from src.utils.headers import github
from src.utils import tracker

class PrsAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prsall')
    async def prsall(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        await ctx.send(embed=success('starting bulk pr import...'))
        
        channel = self.bot.get_channel(config.channels['prs'])
        if not channel:
            await ctx.send(embed=error('prs channel not configured'))
            return
        
        async with aiohttp.ClientSession() as session:
            headers = github()
            all_prs = []
            page = 1
            
            while True:
                url = f'https://api.github.com/repos/{config.github_repo}/pulls?state=open&per_page=100&page={page}'
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        prs = await response.json()
                        if not prs:
                            break
                        
                        all_prs.extend(prs)
                        page += 1
                        
                        if page > 10:
                            break
                    else:
                        await ctx.send(embed=error(f'api error: {response.status}'))
                        return
            
            all_prs.sort(key=lambda x: x['created_at'])
            
            await ctx.send(embed=success(f'found {len(all_prs)} prs, checking for duplicates...'))
            
            new_prs = []
            for pr in all_prs:
                existing = tracker.get('prs', pr['number'])
                if not existing:
                    new_prs.append(pr)
            
            if not new_prs:
                await ctx.send(embed=success('all prs already posted'))
                return
            
            await ctx.send(embed=success(f'posting {len(new_prs)} new prs...'))
            
            posted = 0
            for pr in new_prs:
                try:
                    pr_url = f'https://api.github.com/repos/{config.github_repo}/pulls/{pr["number"]}'
                    async with session.get(pr_url, headers=headers) as response:
                        if response.status == 200:
                            full_pr = await response.json()
                            message = await channel.send(embed=formatpr(full_pr))
                            tracker.track('prs', pr['number'], message.id, channel.id)
                            posted += 1
                    
                    if posted % 50 == 0:
                        print(f'posted {posted}/{len(new_prs)} prs')
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f'error posting pr {pr["number"]}: {e}')
                    continue
            
            await ctx.send(embed=success(f'completed! posted {posted} new prs'))

async def setup(bot):
    await bot.add_cog(PrsAll(bot))
import discord
from discord.ext import commands
import aiohttp
import asyncio
from src import config
from src.formatters.embed import formatissue
from src.utils.embed import error, success
from src.utils.headers import github
from src.utils import tracker

class IssuesAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='issuesall')
    async def issuesall(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        await ctx.send(embed=success('starting bulk issue import...'))
        
        channel = self.bot.get_channel(config.channels['issues'])
        if not channel:
            await ctx.send(embed=error('issues channel not configured'))
            return
        
        async with aiohttp.ClientSession() as session:
            headers = github()
            all_issues = []
            page = 1
            
            while True:
                url = f'https://api.github.com/repos/{config.github_repo}/issues?state=open&per_page=100&page={page}'
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        issues = await response.json()
                        if not issues:
                            break
                        
                        real_issues = [i for i in issues if 'pull_request' not in i]
                        all_issues.extend(real_issues)
                        page += 1
                        
                        if page > 10:
                            break
                    else:
                        await ctx.send(embed=error(f'api error: {response.status}'))
                        return
            
            all_issues.sort(key=lambda x: x['created_at'])
            
            await ctx.send(embed=success(f'found {len(all_issues)} issues, checking for duplicates...'))
            
            new_issues = []
            for issue in all_issues:
                existing = tracker.get('issues', issue['number'])
                if not existing:
                    new_issues.append(issue)
            
            if not new_issues:
                await ctx.send(embed=success('all issues already posted'))
                return
            
            await ctx.send(embed=success(f'posting {len(new_issues)} new issues...'))
            
            posted = 0
            for issue in new_issues:
                try:
                    message = await channel.send(embed=formatissue(issue))
                    tracker.track('issues', issue['number'], message.id, channel.id)
                    posted += 1
                    
                    if posted % 50 == 0:
                        print(f'posted {posted}/{len(new_issues)} issues')
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f'error posting issue {issue["number"]}: {e}')
                    continue
            
            await ctx.send(embed=success(f'completed! posted {posted} new issues'))

async def setup(bot):
    await bot.add_cog(IssuesAll(bot))
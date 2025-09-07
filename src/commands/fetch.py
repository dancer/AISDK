import discord
from discord.ext import commands
import aiohttp
from src import config
from src.formatters.embed import formatpr, formatissue, formatrelease
from src.utils.embed import error
from src.utils.headers import github

class Fetch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fetch')
    async def fetch(self, ctx, number: str):
        if ctx.author.id != config.owner_id:
            return
        
        number = number.lstrip('#')
        try:
            number = int(number)
        except ValueError:
            await ctx.send(embed=error('invalid number format'))
            return
        
        async with aiohttp.ClientSession() as session:
            headers = github()
            
            issue_url = f'https://api.github.com/repos/{config.github_repo}/issues/{number}'
            async with session.get(issue_url, headers=headers) as response:
                if response.status == 200:
                    issue = await response.json()
                    if 'pull_request' in issue:
                        pr_url = f'https://api.github.com/repos/{config.github_repo}/pulls/{number}'
                        async with session.get(pr_url, headers=headers) as pr_response:
                            if pr_response.status == 200:
                                pr = await pr_response.json()
                                await ctx.send(embed=formatpr(pr))
                            else:
                                await ctx.send(embed=formatpr(issue))
                    else:
                        await ctx.send(embed=formatissue(issue))
                    return
                elif response.status == 404:
                    pass
                else:
                    await ctx.send(embed=error(f'api error: {response.status}'))
                    return
            
            release_url = f'https://api.github.com/repos/{config.github_repo}/releases/tags/{number}'
            async with session.get(release_url, headers=headers) as response:
                if response.status == 200:
                    release = await response.json()
                    await ctx.send(embed=formatrelease(release))
                    return
            
            await ctx.send(embed=error(f'not found: #{number}'))

async def setup(bot):
    await bot.add_cog(Fetch(bot))
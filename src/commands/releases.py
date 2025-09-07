import discord
from discord.ext import commands
import aiohttp
from src import config
from src.formatters.embed import formatrelease
from src.utils.embed import error
from src.utils.headers import github

class Releases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='releases')
    async def releases(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        async with aiohttp.ClientSession() as session:
            headers = github()
            url = f'https://api.github.com/repos/{config.github_repo}/releases/latest'
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    release = await response.json()
                    await ctx.send(embed=formatrelease(release))
                elif response.status == 404:
                    await ctx.send(embed=error('no releases found'))
                else:
                    await ctx.send(embed=error(f'api error: {response.status}'))

async def setup(bot):
    await bot.add_cog(Releases(bot))
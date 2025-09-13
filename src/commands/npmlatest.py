import discord
from discord.ext import commands
import aiohttp
from src import config
from src.formatters.embed import formatnpm
from src.utils.embed import error

class Npmlatest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='npmlatest')
    async def npmlatest(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        async with aiohttp.ClientSession() as session:
            url = f'https://registry.npmjs.org/{config.npm_package}'
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    latest = data['dist-tags']['latest']
                    await ctx.send(embed=formatnpm(latest, data['versions'][latest]))
                else:
                    await ctx.send(embed=error(f'api error: {response.status}'))

async def setup(bot):
    await bot.add_cog(Npmlatest(bot))
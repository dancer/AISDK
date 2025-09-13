import discord
from discord.ext import commands
import aiohttp
import asyncio
from src import config
from src.formatters.embed import formatnpm
from src.utils.embed import error
from src.utils import tracker

class Npmall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='npmall')
    async def npmall(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        async with aiohttp.ClientSession() as session:
            url = f'https://registry.npmjs.org/{config.npm_package}'
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    versions = list(data['versions'].keys())
                    
                    for version in versions:
                        if not tracker.hasreleasebeensent(version):
                            embed = formatnpm(version, data['versions'][version])
                            message = await ctx.send(embed=embed)
                            tracker.track('releases', version, message.id, ctx.channel.id)
                            await asyncio.sleep(1)
                    
                    await ctx.send(f'sent {len(versions)} npm releases')
                else:
                    await ctx.send(embed=error(f'api error: {response.status}'))

async def setup(bot):
    await bot.add_cog(Npmall(bot))
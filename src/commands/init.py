import discord
from discord.ext import commands
from datetime import datetime, timedelta
from src import config
from src.utils import state
from src.utils.embed import success

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='init')
    async def init(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        now = datetime.now().astimezone()
        yesterday = now - timedelta(days=1)
        
        state.last_check['pr'] = yesterday
        state.last_check['issue'] = yesterday
        state.last_check['release'] = yesterday
        state.last_check['npm'] = yesterday
        state.save(state.last_check)
        
        await ctx.send(embed=success('initialized timestamps to 24 hours ago'))

async def setup(bot):
    await bot.add_cog(Init(bot))
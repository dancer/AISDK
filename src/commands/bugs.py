import discord
from discord.ext import commands
from src import config

class Bugs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bugs')
    async def bugs(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        embed = discord.Embed(
            title='Bug Reporting',
            description='Found a bug? Help us improve!',
            color=0x000000
        )
        
        embed.add_field(
            name='How to Report',
            value='Please report bugs on our GitHub Issues page:\n[github.com/vercel/ai/issues](https://github.com/vercel/ai/issues)',
            inline=False
        )
        
        embed.add_field(
            name='Before Reporting',
            value='• Search existing issues to avoid duplicates\n• Check the documentation at [ai-sdk.dev](https://ai-sdk.dev)\n• Verify you\'re using the latest version',
            inline=False
        )
        
        embed.add_field(
            name='What to Include',
            value='• Clear description of the issue\n• Steps to reproduce\n• Expected vs actual behavior\n• Code snippets if applicable',
            inline=False
        )
        
        embed.set_footer(text='▲ Vercel x AI SDK')
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Bugs(bot))
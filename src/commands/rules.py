import discord
from discord.ext import commands
from src import config

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rules')
    async def rules(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        embed = discord.Embed(
            title='Server Rules',
            color=0xFFFFFF
        )
        
        embed.add_field(
            name='1. reporting issues',
            value='found a bug or issue with the ai sdk? please report it on [github issues](https://github.com/vercel/ai/issues)',
            inline=False
        )
        
        embed.add_field(
            name='2. asking questions',
            value='have questions about the ai sdk? ask in <#1414092320046846062>',
            inline=False
        )
        
        embed.add_field(
            name='3. stay on topic',
            value='keep discussions related to vercel ai sdk and ai development',
            inline=False
        )
        
        embed.add_field(
            name='4. be respectful',
            value='treat all members with respect and maintain professional conduct',
            inline=False
        )
        
        embed.add_field(
            name='5. no spam',
            value='avoid duplicate messages, excessive mentions, or promotional content',
            inline=False
        )
        
        embed.add_field(
            name='6. use appropriate channels',
            value='post in the correct channels to keep discussions organized',
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rules(bot))
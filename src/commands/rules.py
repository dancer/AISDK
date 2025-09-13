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
        
        embed.set_footer(text='▲ Vercel x AI SDK')
        
        embed.add_field(
            name='1. Reporting Issues',
            value='Found a bug or issue with the AI SDK? Please report it on [GitHub Issues](https://github.com/vercel/ai/issues)',
            inline=False
        )
        
        embed.add_field(
            name='2. Asking Questions',
            value='Have questions about the AI SDK? Ask in <#1414092320046846062>',
            inline=False
        )
        
        embed.add_field(
            name='3. Stay on Topic',
            value='Keep discussions related to Vercel AI SDK and AI development',
            inline=False
        )
        
        embed.add_field(
            name='4. Be Respectful',
            value='Treat all members with respect and maintain professional conduct',
            inline=False
        )
        
        embed.add_field(
            name='5. No Spam',
            value='Avoid duplicate messages, excessive mentions, or promotional content',
            inline=False
        )
        
        embed.add_field(
            name='6. Use Appropriate Channels',
            value='Post in the correct channels to keep discussions organized',
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rules(bot))
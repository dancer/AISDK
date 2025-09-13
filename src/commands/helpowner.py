import discord
from discord.ext import commands
from src import config

class Helpowner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='helpowner')
    async def helpowner(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        embed = discord.Embed(
            title='All Commands',
            description='Complete list of available commands',
            color=0x000000
        )
        
        embed.add_field(
            name='Public Commands',
            value='`?help` - Show help information',
            inline=False
        )
        
        embed.add_field(
            name='Owner Commands',
            value='`?init` - Initialize bot settings\n`?fetch` - Fetch PRs/issues from GitHub\n`?prsall` - Send all PRs to channel\n`?issuesall` - Send all issues to channel\n`?npmall` - Send all npm releases to channel\n`?npmlatest` - Show latest npm release\n`?releases` - Show latest GitHub release\n`?rules` - Display server rules\n`?welcome` - Send welcome message\n`?bugs` - Show bug reporting guide\n`?helpowner` - This command',
            inline=False
        )
        
        embed.set_footer(text='▲ Vercel x AI SDK')
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Helpowner(bot))
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        from src import config
        
        embed = discord.Embed(
            title='AI SDK Monitor',
            color=0xFFFFFF
        )
        
        prs_channel = f'<#{config.channels["prs"]}>' if config.channels['prs'] else '#prs'
        issues_channel = f'<#{config.channels["issues"]}>' if config.channels['issues'] else '#issues'
        releases_channel = f'<#{config.channels["releases"]}>' if config.channels['releases'] else '#releases'
        
        embed.add_field(
            name='monitoring',
            value=f'• [pull requests](https://github.com/vercel/ai/pulls) → {prs_channel}\n• [issues](https://github.com/vercel/ai/issues) → {issues_channel}\n• [npm releases](https://www.npmjs.com/package/ai) → {releases_channel}',
            inline=False
        )
        
        embed.add_field(
            name='frequency',
            value='checks every 30 seconds',
            inline=False
        )
        
        embed.add_field(
            name='repository',
            value='[github.com/vercel/ai](https://github.com/vercel/ai)',
            inline=True
        )
        
        embed.add_field(
            name='npm package',
            value='[npmjs.com/package/ai](https://www.npmjs.com/package/ai)',
            inline=True
        )
        
        embed.set_footer(text='ai sdk monitor • ?help')
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
import discord
from discord.ext import commands
from src import config

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='welcome')
    async def welcome(self, ctx):
        if ctx.author.id != config.owner_id:
            return
        
        embed = discord.Embed(
            title='Welcome!!!',
            description='To the [AI SDK](https://ai-sdk.dev) discord server',
            color=0xFFFFFF
        )
        
        embed.set_image(url='https://media.discordapp.net/attachments/1412487599469232208/1414110949371285614/1500x500.png?ex=68be60f3&is=68bd0f73&hm=6fef646fa9e9e593a939fca0c35626302d22e127ced5829a5ef81e3e6709fba0&=&format=webp&quality=lossless&width=1714&height=571')
        
        embed.add_field(
            name='Community',
            value='You can check out more about our community at [community.vercel.com](https://community.vercel.com/)',
            inline=False
        )
        
        embed.add_field(
            name='Getting started',
            value='Please verify with the emoji below and please follow the rules!',
            inline=False
        )
        
        embed.set_footer(text='▲ Vercel x AI SDK')
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
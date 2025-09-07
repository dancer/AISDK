import discord
from discord.ext import commands, tasks
from src import config
from src.monitors.github import checkprs, checkissues, checkreleases
from src.monitors.npm import checknpm

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} connected')
    await bot.load_extension('src.commands.help')
    await bot.load_extension('src.commands.fetch')
    await bot.load_extension('src.commands.releases')
    await bot.load_extension('src.commands.issuesall')
    await bot.load_extension('src.commands.prsall')
    await bot.load_extension('src.commands.init')
    await bot.load_extension('src.commands.rules')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='vercel/ai'))
    monitor.start()

@tasks.loop(seconds=30)
async def monitor():
    await checkprs(sendwebhook, bot)
    await checkissues(sendwebhook, bot)
    await checkreleases(sendwebhook, bot)
    await checknpm(sendwebhook, bot)

async def sendwebhook(channel_type, embed, item_type=None, number=None):
    channel_id = config.channels[channel_type]
    if channel_id and (channel := bot.get_channel(channel_id)):
        message = await channel.send(embed=embed)
        if item_type and number:
            from src.utils import tracker
            tracker.track(item_type, number, message.id, channel_id)
        return message

def run():
    bot.run(config.token)
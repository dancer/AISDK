import discord
from discord.ext import commands, tasks
from src import config
from src.monitors.github import checkprs, checkissues
from src.monitors.npm import checknpm

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} connected')
    await bot.load_extension('src.commands.help')
    await bot.load_extension('src.commands.helpowner')
    await bot.load_extension('src.commands.fetch')
    await bot.load_extension('src.commands.releases')
    await bot.load_extension('src.commands.issuesall')
    await bot.load_extension('src.commands.prsall')
    await bot.load_extension('src.commands.init')
    await bot.load_extension('src.commands.rules')
    await bot.load_extension('src.commands.welcome')
    await bot.load_extension('src.commands.bugs')
    await bot.load_extension('src.commands.npmlatest')
    await bot.load_extension('src.commands.npmall')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='▲'))
    monitor.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.channel.id == config.channels.get('ai'):
        if message.content.lower() == 'ai':
            emoji = bot.get_emoji(1416231482497826870)
            if emoji:
                await message.add_reaction(emoji)
        else:
            await message.delete()
        return
    
    await bot.process_commands(message)

@tasks.loop(seconds=30)
async def monitor():
    await checkprs(sendwebhook, bot)
    await checkissues(sendwebhook, bot)
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
import discord

def error(message):
    return discord.Embed(
        description=message,
        color=0xFFFFFF
    )

def success(message):
    return discord.Embed(
        description=message,
        color=0xFFFFFF
    )
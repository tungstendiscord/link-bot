import discord
from discord.ext import commands

client = commands.Bot(command_prefix="l!", help_command=None)

async def set_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="commands that start with l!"))

initial_extensions = ['cogs.dictionary']
for extension in initial_extensions:
    client.load_extension(extension)

@client.event
async def on_ready():
    print("Ready!")
    await set_status()

@commands.guild_only()
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! :ping_pong: My latency is `{round(client.latency * 1000, 2)}`ms.")

client.run("")
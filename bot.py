import os
import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_TOKEN"]
ROLE_NAME = os.environ.get("ROLE_NAME", "YOUR_ROLE_NAME_HERE")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def role(ctx):
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    if role is None:
        await ctx.send(f"Role '{ROLE_NAME}' not found.")
        return
    if role in ctx.author.roles:
        await ctx.send(f"You already have the **{ROLE_NAME}** role.")
        return
    await ctx.author.add_roles(role)
    await ctx.send(f"✅ Gave you the **{ROLE_NAME}** role!")

bot.run(TOKEN)

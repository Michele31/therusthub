import os
import discord
from discord.ext import commands
from discord.ext import tasks

TOKEN = os.environ["DISCORD_TOKEN"]
ROLE_NAME = os.environ.get("ROLE_NAME", "YOUR_ROLE_NAME_HERE")
COUNTER_CHANNEL_ID = int(os.environ.get("COUNTER_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def update_counter(guild):
    if COUNTER_CHANNEL_ID == 0:
        return
    channel = guild.get_channel(COUNTER_CHANNEL_ID)
    if channel is None:
        return
    count = sum(1 for m in guild.members if not m.bot)
    await channel.edit(name=f"Members: {count}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        await update_counter(guild)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)
    if role:
        await member.add_roles(role)
    await update_counter(member.guild)

@bot.event
async def on_member_remove(member):
    await update_counter(member.guild)

@bot.command()
@commands.has_permissions(administrator=True)
async def role(ctx):
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    if role is None:
        await ctx.send(f"Role '{ROLE_NAME}' not found.")
        return
    members = [m for m in ctx.guild.members if not m.bot and role not in m.roles]
    if not members:
        await ctx.send(f"Everyone already has the **{ROLE_NAME}** role.")
        return
    await ctx.send(f"Assigning **{ROLE_NAME}** to {len(members)} members...")
    failed = 0
    for member in members:
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            failed += 1
        except discord.HTTPException:
            failed += 1
    success = len(members) - failed
    await ctx.send(f"✅ Done! Gave **{ROLE_NAME}** to {success}/{len(members)} members." + (f" ({failed} failed — check bot role hierarchy)" if failed else ""))

@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permission to use this command.")

bot.run(TOKEN)

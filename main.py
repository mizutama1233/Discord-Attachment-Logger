# https://github.com/mizutama1233
import disnake
from disnake.ext import commands

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True
intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("[-]"), command_sync_flags=command_sync_flags, intents=intents)

tasks = {}

CHANNEL_ID = 0
GUILD_ID = 0

@bot.slash_command(description="setup Attachment logger")
async def setup(ctx, channel: disnake.TextChannel):
  global CHANNEL_ID
  global GUILD_ID
  CHANNEL_ID = channel.id
  GUILD_ID = ctx.guild.id
  tasks[GUILD_ID] = CHANNEL_ID
  await ctx.send("Setup is ended.\nLogs are sent to this channel here")

@bot.event
async def on_message(message):
  if len(message.attachments) > 0:
    for attachment in message.attachments:
      channel = bot.get_channel(tasks[message.guild.id])
      await channel.send(f"Attachment is Detected in <#{message.channel.id}>\n{attachment.url}")

@bot.slash_command(description="Stop Attachment Logger")
async def stop(ctx):
  try:
    del tasks[ctx.guild.id]
    await ctx.send("Success")
  except KeyError:
    await ctx.send("Already deleted or does not exist")

TOKEN = "Your token"
bot.run(TOKEN)

import os
import logging

import disnake
from disnake.ext import commands

logging.basicConfig(level=logging.WARNING)

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="m.", intents=intents, test_guilds=[777620282574766110])
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="Miko Family"))

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run("ODc2NzkzNzg2NDI3MTI5ODc2.Gaycsg.QWehXXXPlfDxXzAXIMoZSLRnWGfeDpstzyiJ2Y")

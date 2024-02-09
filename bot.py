import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks


extens = ["cogs.loops", "cogs.slash_commands"]


class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        print(f"{self.user} is now running!")
        for cog in extens:
            try:
                await bot.load_extension(cog)
                print(f"{cog} was loaded.")
            except Exception as e:
                print(e)


bot = MyBot()
load_dotenv()
bot.run(os.getenv('TOKEN'))
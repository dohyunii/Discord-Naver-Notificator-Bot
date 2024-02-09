import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import logic


class SlashCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx) -> None:
        if ctx.author.id == 434005581234438152:
            fmt = await self.bot.tree.sync()
            await ctx.send(f'Synced {len(fmt)} commands!')
        else:
            await ctx.send("You must be the owner to use this command!")

    @app_commands.command(name="add", description="Adding the title to notifications.")
    async def add(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer()
        await asyncio.sleep(2)
        await interaction.followup.send(logic.add(link, interaction.channel.id))

    @app_commands.command(name="list", description="Shows the titles you added to notifications.")
    async def list(self, interaction: discord.Interaction):
        await interaction.response.send_message(logic.list_of_titles(interaction.channel.id))

    @app_commands.command(name="remove", description="Removes the title from notifications.")
    async def remove(self, interaction: discord.Interaction, list_number: int):
        await interaction.response.send_message(logic.remove(list_number, interaction.channel.id))


async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
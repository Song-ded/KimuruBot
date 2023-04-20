import random

import disnake
from disnake.ext import commands


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def avatar(self, interaction, member: disnake.Member = None):
        colour=random.randint(0, 16777215)
        user = member or interaction.author
        embed = disnake.Embed(title='Аватар', color = colour)
        embed.set_image(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Avatar(bot))
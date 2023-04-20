import disnake
from disnake.ext import commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ban(self, interaction, user: disnake.User, reason: str = None):
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(f"Забанен {user.mention}", ephemeral = True)

    @commands.slash_command()
    async def ban(self, interaction, user: disnake.User):
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Разбанен {user.mention}", ephemeral = True)


def setup(bot):
    bot.add_cog(Ban(bot))
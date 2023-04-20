import datetime
import random

import disnake
from disnake.ext import commands


class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def timeout(self, interaction, member: disnake.Member, time: str, reason: str):
        colour=random.randint(0, 16777215)
        time = datetime.datetime.now() + datetime.timedelta(minutes=int(time))
        await member.timeout(reason=reason, until=time)
        cool_time = disnake.utils.format_dt(time, style="R")
        embed = disnake.Embed(title="Таймаут", description = f"{member.mention} будет прерван {cool_time}", color = colour)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command()
    async def untimeout(self, interaction, member: disnake.Member):
        await member.timeout(reason=None, until=None)
        await interaction.response.send_message(f"Снят таймаут {member.mention}", ephemeral = True)

def setup(bot):
    bot.add_cog(Timeout(bot))
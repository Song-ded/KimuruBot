import disnake
from disnake.ext import commands


class Welcome_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        channel = member.guild.system_channel
        embed = disnake.Embed(color = 0x2ecc71, title=f"Miko Family", description=f"{member.mention} Приветствуем тебя на сервере!")
        embed.set_footer(text=f"Miko Family", icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome_message(bot))
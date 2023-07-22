import disnake
from disnake.ext import commands

class Mathfunc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='калькулятор', description='Внутренний калькулятор')
    async def calc(self, interaction, arg: str):
        try:
            result = eval(arg)
            embed = disnake.Embed(color=0x2ecc71, title='Калькулятор', description=f"{interaction.user.mention} Результат: {result}")
            embed.set_footer(text=arg, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except:
            embed = disnake.Embed(color=0xe74c3c, title='Калькулятор', description=f"{interaction.user.mention} Произошла ошибка")
            embed.set_footer(text=arg, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
def setup(bot):
    bot.add_cog(Mathfunc(bot))
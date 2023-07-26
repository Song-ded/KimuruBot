import disnake
from disnake.ext import commands
from utils.databases import UsersDataBase
class Lovepy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.slash_command(name='письмо', description='Написать анонимное письмо человеку [Цена 100]')
    async def anonim(self, interaction, member: disnake.Member, text: str):
        await self.db.create_table()
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        if 100 <= user[1]:
            embed = disnake.Embed(title="Письмо✉️", description=text, color = 0x2ecc71)
            embed.set_thumbnail(url=member.display_avatar.url)
            try:
                await member.send(embed=embed)
            except:
                await interaction.response.send_message('Все в порядке, но.. У человека видимо закрыто ЛС😢', ephemeral=True)
        else:
            embed = disnake.Embed(title=f'Анонимное письмо - {member}', description="У вас не хватает денег!", color=0xe74c3c)
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
def setup(bot):
    bot.add_cog(Lovepy(bot))
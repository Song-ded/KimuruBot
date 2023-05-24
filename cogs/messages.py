import disnake
from disnake.ext import commands

from datetime import datetime
from utils.databases import UsersDataBase
class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.author)
        if message.author.bot != True:
            print(1)
            await self.db.create_table2()
            print(2)
            await self.db.add_ustats(message.author)
            print(3)
            await self.db.update_stats(message.author, 1)
            print(4)
        else:
            pass

    @commands.slash_command(name='сообщения', description='Узнать сколько вы написали сообщений')
    async def mess(self, interaction):
        await self.db.create_table2()
        await self.db.add_ustats(interaction.author)
        user = await self.db.get_stats(interaction.author)
        await interaction.response.send_message(user[1], ephemeral=True)

    @commands.slash_command(name='награда', description='Получить награду')
    async def award(self, interaction, arg=commands.Param(choices=['Активный', 'Долгожитель'])):
        if arg == 'Активный':
            await self.db.create_table2()
            await self.db.add_ustats(interaction.author)
            user = await self.db.get_stats(interaction.author)
            if user[1] >= 300:
                role = interaction.guild.get_role(917022395552915476)
                await interaction.user.add_roles(role, reason=None)
                await interaction.response.send_message('Вы успешно получили награду **Активный**!', ephemeral=True)
            else:
                await interaction.response.send_message('Для получения награды **Активный**, вам требуется написать на сервере 300 сообщений!', ephemeral=True)
        elif arg == 'Долгожитель':
            value0 = datetime.today()
            value1 = interaction.user.joined_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            value2 = datetime.strptime(value1, '%Y-%m-%d %H:%M:%S.%f')
            if (value0 - value2).days >= 300:
                role = interaction.guild.get_role(987712822580490250)
                await interaction.user.add_roles(role, reason=None)
                await interaction.response.send_message('Вы успешно получили награду **Долгожитель**!', ephemeral=True)
            else:
                await interaction.response.send_message('Для получения награды **Долгожитель**, вам требуется пробыть на сервере не покидая его 300 суток!', ephemeral=True)
def setup(bot):
    bot.add_cog(Messages(bot))

import disnake
from disnake.ext import commands

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
def setup(bot):
    bot.add_cog(Messages(bot))
import disnake
from disnake.ext import commands

from datetime import datetime
from utils.databases import UsersDataBase


class PaginatorView(disnake.ui.View):
    def __init__(self, embeds, author, footer: bool, timeout=30.0):
        self.embeds = embeds
        self.author = author
        self.footer = footer
        self.timeout = timeout
        self.page = 0
        super().__init__(timeout=self.timeout)

        if self.footer:
            for emb in self.embeds:
                emb.set_footer(text=f'Страница {self.embeds.index(emb) + 1} из {len(self.embeds)}')

    @disnake.ui.button(label='◀️', style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == 0:
                self.page = len(self.embeds) - 1
            else:
                self.page -= 1
        else:
            return

        await self.button_callback(interaction)

    @disnake.ui.button(label='▶️', style=disnake.ButtonStyle.grey)
    async def next(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == len(self.embeds) - 1:
                self.page = 0
            else:
                self.page += 1
        else:
            return

        await self.button_callback(interaction)

    async def button_callback(self, interaction):
        if self.author.id == interaction.author.id:
            await interaction.response.edit_message(embed=self.embeds[self.page])
        else:
            return await interaction.response.send_message('Вы не можете использовать эту кнопку!', ephemeral=True)

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.slash_command(name='топ_по_сообщениям', description='Посмотреть топ пользователей по сообщениям')
    async def top_message(self, interaction):
        await self.db.create_table2()
        top = await self.db.get_messagestop()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}.** {self.bot.get_user(user[0])} - {user[1]} 💬\n'
            if loop_count % 10 == 0 or loop_count - 1 == len(top) - 1:
                embed = disnake.Embed(title='Топ пользователей')
                embed.description = text
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                embeds.append(embed)
                text = ''
        view = PaginatorView(embeds, interaction.author, True)
        await interaction.response.send_message(embed=embeds[0], view=view)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot != True:
            await self.db.create_table2()
            await self.db.create_table()
            await self.db.add_user(message.author)
            await self.db.add_ustats(message.author)
            res = len(message.content)
            user = message.author
            role = disnake.utils.find(lambda r: r.name == '⌊😎⌉│Server Booster', message.guild.roles)
            if role in user.roles:
                rest = int(res) * 0.5
            else:
                rest = int(res) * 0.2
            await self.db.update_money(message.author, int(rest), 0)
            await self.db.update_stats(message.author, 1)
        else:
            pass
        try:
            if message.interaction.name == "remaining":
                if 'Времени до' in message.embeds[0].description:
                    user = message.interaction.user
                    await self.db.create_table()
                    await self.db.add_user(user)
                    await self.db.update_money(user, 500, 0)
                    embed = disnake.Embed(title="Спасибо за лайк сервера!", description=f"{user} вы получили 500🪙 за лайк сервера!", color = 0x2ecc71)
                    await message.channel.send(embed=embed)
            if message.interaction.name == "up":
                if 'Успешный Up!' in message.embeds[0].description:
                    user = message.interaction.user
                    await self.db.create_table()
                    await self.db.add_user(user.id)
                    await self.db.update_money(user.id, 500, 0)
                    embed = disnake.Embed(title="Спасибо за ап сервера!", description=f"{user} вы получили 500🪙 за ап сервера!", color = 0x2ecc71)
                    await message.channel.send(embed=embed)
            elif message.interaction.name == "like":
                if 'Вы успешно лайкнули сервер.' in message.embeds[0].description:
                    user = message.interaction.user
                    await self.db.create_table()
                    await self.db.add_user(user.id)
                    await self.db.update_money(user.id, 500, 0)
                    embed = disnake.Embed(title="Спасибо за лайк сервера!", description=f"{user} вы получили 500🪙 за лайк сервера!", color = 0x2ecc71)
                    await message.channel.send(embed=embed)
            elif message.interaction.name == "bump":
                 if 'Bump done!' in message.embeds[0].description:
                    user = message.interaction.user
                    await self.db.create_table()
                    await self.db.add_user(user.id)
                    await self.db.update_money(user.id, 250, 0)
                    embed = disnake.Embed(title="Спасибо за бамп сервера!", description=f"{user} вы получили 250🪙 за бамп сервера!", color = 0x2ecc71)
                    await message.channel.send(embed=embed)
        except:
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

    @commands.slash_command(name='сообщение', description='Написать сообщение от лица бота')
    async def messbot(self, interaction, chan = int, arg= str):
        channel = interaction.guild.get_channel(chan)
        await interaction.channel.send(arg)


def setup(bot):
    bot.add_cog(Messages(bot))

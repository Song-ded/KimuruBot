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
            if self.bot.get_user(user[0]) == None:
                pass
            else:
                n += 1
                string = f"{self.bot.get_user(user[0])}"
                string1 = string.replace("#0","")
                loop_count += 1
                text += f'**{n}.** {string1} - {user[1]} 💬\n'
                if n >= 51:
                    pass
                else:
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
            user = message.author
            await self.db.create_table()
            await self.db.add_user(user)
            res = len(message.content)
            us = await self.db.get_stats(user)
            await self.db.create_table2()
            await self.db.add_ustats(message.author)
            us = await self.db.get_stats(message.author)
            if us[1] >= 350:
                role = message.guild.get_role(1139173666874208296)
                await message.author.add_roles(role, reason=None)
            try:
                role = disnake.utils.find(lambda r: r.name == '⌊😎⌉│Server Booster', message.guild.roles)
            except:
                pass
            if role in user.roles:
                rest = int(res) * 0.1
            else:
                rest = int(res) * 0.03
            if message.channel.id == "1134926324000104490":
                pass
            else:
                await self.db.update_money(user, int(rest), 0)
                await self.db.update_stats(user, 1)
        try:
            if message.interaction.name == "up":
                if 'Время' in message.embeds[0].field[0].value:
                    user = message.interaction.user
                    await self.db.create_table()
                    await self.db.add_user(user)
                    await self.db.update_money(user, 500, 0)
                    embed = disnake.Embed(title="Спасибо за ап сервера!", description=f"{user} вы получили 500🪙 за ап сервера!", color = 0x2ecc71)
                    await message.channel.send(embed=embed)
            elif message.interaction.name == "like":
                if 'Вы успешно лайкнули сервер.' in message.embeds[0].description:
                    user = message.interaction.user
                    await self.db.create_table()
                    await self.db.add_user(user)
                    await self.db.update_money(user, 500, 0)
                    embed = disnake.Embed(title="Спасибо за лайк сервера!", description=f"{user} вы получили 500🪙 за лайк сервера!", color = 0x2ecc71)
                    await message.channel.send(embed=embed)
            elif message.interaction.name == "bump":
                 if 'Bump done!' in message.embeds[0].description:
                    user = message.interaction.user
                    await self.db.create_table()
                    await self.db.add_user(user)
                    await self.db.update_money(user, 250, 0)
                    embed = disnake.Embed(title="Спасибо за бамп сервера!", description=f"{user} вы получили 250🪙 за бамп сервера!", color = 0x2ecc71)
                    await message.channel.send(embed=embed)
        except:
            pass

    @commands.slash_command(name='сообщения', description='Узнать сколько вы написали сообщений')
    async def mess(self, interaction, member: disnake.Member):
        if member is None:
            member = interaction.author
        await self.db.create_table2()
        await self.db.add_ustats(member)
        user = await self.db.get_stats(member)
        await interaction.response.send_message(user[1], ephemeral=True)
	
    @commands.slash_command(name='выдатьсооб', description='Выдать сооб пользователю')
    async def give123(self, interaction, member: disnake.Member, amount: int):
        await self.db.create_table2()
        await self.db.add_ustats(member)
        await self.db.update_stats(member, amount)
        await interaction.response.send_message('Готово', ephemeral=True)
    
    @commands.slash_command(name='награда', description='Получить награду')
    async def award(self, interaction, arg=commands.Param(choices=['Активный', 'Долгожитель'])):
        if arg == 'Активный':
            await self.db.create_table2()
            await self.db.add_ustats(interaction.author)
            user = await self.db.get_stats(interaction.author)
            if user[1] >= 1000:
                role = interaction.guild.get_role(917022395552915476)
                await interaction.user.add_roles(role, reason=None)
                await interaction.response.send_message('Вы успешно получили награду **Активный**!', ephemeral=True)
            else:
                await interaction.response.send_message('Для получения награды **Активный**, вам требуется написать на сервере 1000 сообщений!', ephemeral=True)
        elif arg == 'Долгожитель':
            value0 = datetime.today()
            value1 = interaction.user.joined_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            value2 = datetime.strptime(value1, '%Y-%m-%d %H:%M:%S.%f')
            if (value0 - value2).days >= 200:
                role = interaction.guild.get_role(987712822580490250)
                await interaction.user.add_roles(role, reason=None)
                await interaction.response.send_message('Вы успешно получили награду **Долгожитель**!', ephemeral=True)
            else:
                await interaction.response.send_message('Для получения награды **Долгожитель**, вам требуется пробыть на сервере не покидая его 200 суток!', ephemeral=True)

    @commands.slash_command(name='сообщение', description='Написать сообщение от лица бота')
    async def messbot(self, interaction, chan = int, arg= str):
        channel = interaction.guild.get_channel(chan)
        await interaction.channel.send(arg)


def setup(bot):
    bot.add_cog(Messages(bot))
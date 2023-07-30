import disnake
from disnake.ext import commands

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


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.slash_command(name='баланс', description='Посмотреть баланс')
    async def balance(self, interaction, member: disnake.Member = None):
        await self.db.create_table()
        if not member:
            member = interaction.author
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        embed = disnake.Embed(title=f'Баланс пользователя - {member}')
        embed.add_field(name='🪙 Деньги', value=f'```{user[1]}```')
        embed.add_field(name='💎 Премиум', value=f'```{user[2]}```')
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)


    @commands.slash_command(name='обмен', description='Обменять деньги на премиум')
    async def exchange(self, interaction, amount: int, member = None, exchange=commands.Param(choices=['деньги', 'премиум'])):
        if member == None:
            member = interaction.author
        await self.db.create_table()
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        if exchange == 'премиум':
            perm = amount * 10000
            if perm <= user[1]:
                await self.db.update_money(member, (amount - perm) - 1, amount)
                embed = disnake.Embed(title=f'Обмен - {member}', description="Операция прошла успешно!", color = 0x2ecc71)
                embed.set_thumbnail(url=member.display_avatar.url)
                await interaction.response.send_message(embed=embed)
            else:
                embed = disnake.Embed(title=f'Обмен - {member}', description="Операция провалена!", color = 0xe74c3c)
                embed.set_thumbnail(url=member.display_avatar.url)
                await interaction.response.send_message(embed=embed)
        elif exchange=='деньги':
            perm = amount / 10000
            if amount > 9999 and perm <= user[2]:
                if perm < user[2]:
                    await self.db.update_money(member, amount - 0, -abs(perm)) # деньги
                    embed = disnake.Embed(title=f'Обмен - {member}', description="Операция прошла успешно!", color = 0x2ecc71)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = disnake.Embed(title=f'Обмен - {member}', description="Операция провалена!", color = 0xe74c3c)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='выдать', description='Выдать деньги пользователю')
    async def give(self, interaction, member: disnake.Member,
                   amount: float, arg=commands.Param(choices=['деньги', 'премиум'])):
        await self.db.create_table()
        await self.db.add_user(member)
        if arg == 'деньги':
            int(amount)
            await self.db.update_money(member, amount, 0)
            embed = disnake.Embed(title=f'Выдача денег пользователю - {member}')
            embed.description = f'{interaction.author.mention} выдал {member.mention} {amount} денег.'
            embed.set_thumbnail(url=member.display_avatar.url)
        else:
            await self.db.update_money(member, 0, amount)
            embed = disnake.Embed(title=f'Выдача премиума пользователю - {member}')
            embed.description = f'{interaction.author.mention} выдал {member.mention} {amount} премиума.'
            embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)


    @commands.slash_command(name='дать', description='Передать премиум-деньги пользователю')
    async def give_user(self, interaction, member: disnake.Member,
                   amount: float):
        await self.db.create_table()
        await self.db.add_user(member)
        await self.db.add_user(interaction.user)
        user = await self.db.get_user(interaction.user)
        if user[2] <= amount:
            await self.db.update_money(member, 0, amount)
            await self.db.update_money(interaction.user, 0, -abs(amount))
            embed = disnake.Embed(title=f'Передача денег пользователю - {member}')
            embed.description = f'{interaction.author.mention} передал {member.mention} {amount} премиум-денег.'
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(title=f'Передача - {member}', description=f"{interaction.user} Операция провалена!", color=0xe74c3c)
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)


    @commands.slash_command(name='топ_по_валюте', description='Посмотреть топ пользователей по валюте')
    async def top_money(self, interaction):
        await self.db.create_table()
        top = await self.db.get_top()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}.** {self.bot.get_user(user[0])} - {user[1]} 🪙\n'
            if loop_count % 10 == 0 or loop_count - 1 == len(top) - 1:
                embed = disnake.Embed(title='Топ пользователей')
                embed.description = text
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                embeds.append(embed)
                text = ''
        view = PaginatorView(embeds, interaction.author, True)
        await interaction.response.send_message(embed=embeds[0], view=view)

def setup(bot):
    bot.add_cog(Economy(bot))



import disnake
from disnake.ext import commands


class SelectGames(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Модерация"),
            disnake.SelectOption(label="Экономика"),
            disnake.SelectOption(label="РП"),
            disnake.SelectOption(label="Остальное")]
        super().__init__(placeholder="Выберите нужный список команд", options=options, custom_id="help", min_values=0, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        if self.values[0] == "Модерация":
            embed = disnake.Embed(title="Помощь по модерации")
            embed.description = "`/ban` - Забанить пользователя\n" \
            "`/clear` - Очистка сообщений\n" \
            "`/timeout` - Отправить пользователя подумать о своем поведении\n" \
            "`/untimeout` - Отменить пользователю таймаут\n"
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Экономика":
            embed = disnake.Embed(title="Помощь по экономике")
            embed.description = "`/топ` - Посмотреть лидербоард\n" \
            "`/обмен` - Обменивать валюты\n" \
            "`/баланс` - Посмотреть свой/чужой баланс\n" \
            "`/выдать` - Выдать валюту пользователю\n"
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "РП":
            embed = disnake.Embed(title="Помощь по РП")
            embed.description = "`/кусать` - укусить пользователя\n" \
            "`/расстроиться` - выразить эмоцию 'Расстроиться'\n" \
            "`/ударить` - ударить пользователя\n" \
            "`/шлепнуть` - шлепнуть пользователя\n" \
            "`/поцеловать` - поцеловать пользователя\n" \
            "`/обнять` - обнять пользователя\n" \
            "`/пять` - дать пять пользователю\n" \
            "`/не_знать` - выразить эмоцию 'Не знаю'\n" \
            "`/респект` - выразить эмоцию 'Респект'\n" \
            "`/погладить` - погладить пользователя'\n" \
            "`/лизнуть` - лизнуть пользователя\n"
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Остальное":
            embed = disnake.Embed(title="Помощь по Остальное")
            embed.description = "`/заявка` - Подать заявку на должность\n" \
            "`/avatar` - Получить аватар пользователя"
            await interaction.response.send_message(embed=embed, ephemeral=True)
class GameRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.slash_command(name='помощь', description='Посмотреть список команд')
    async def help(self, interaction):
        view = disnake.ui.View(timeout=None)
        view.add_item(SelectGames())
        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name="Помощь:")
        embed.description = f"Приветствую тебя {interaction.author.mention}" \
                            " выберите нужный вам список команд.\n\n"
        await interaction.response.send_message(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(SelectGames())
        self.bot.add_view(view)  # message_id =


def setup(bot):
    bot.add_cog(GameRoles(bot))

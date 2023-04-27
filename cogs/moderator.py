
import disnake
from disnake.ext import commands
from disnake import TextInputStyle

blacklist = [697104275280756846]
for_eventer: bool = True
for_moderator: bool = True

class RecruitementModal(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg  # arg - это аргумент, который передается в конструкторе класса RecruitementSelect
        """
        Также можно сделать так:
                components = [
            disnake.ui.TextInput(label="Ваше имя", placeholder="Введите ваше имя", custom_id="name"),
            disnake.ui.TextInput(label="Был ли у вас опыт в данной сфере?", placeholder="Напишите о вашем опыте, если он есть", custom_id="opt"),
            disnake.ui.TextInput(label="Расскажите о себе", placeholder="Расскажите о себе", custom_id="history"),
            disnake.ui.TextInput(label="Ваш возраст", placeholder="Введите ваш возраст", custom_id="age")
            disnake.ui.TextInput(
                label="Расскажите о себе и почему именно вы?",
                placeholder="Расскажи о себе здесь",
                custom_id="info",
                style=disnake.TextInputStyle.paragraph,
                min_length=10,
                max_length=500,
            )
        ]
        """
        components = [
            disnake.ui.TextInput(label="Ваше имя", placeholder="Введите ваше имя", custom_id="name", style=TextInputStyle.single_line),
            disnake.ui.TextInput(label="Ваш возраст", placeholder="Введите ваш возраст", custom_id="age", max_length=2, min_length=2, style=TextInputStyle.short),
            disnake.ui.TextInput(label="Был ли у вас опыт в данной сфере?", placeholder="Напишите о вашем опыте, если он есть", custom_id="opt", style=TextInputStyle.paragraph, min_length=1, max_length=300),
            disnake.ui.TextInput(label="Расскажите о себе", placeholder="Расскажите о себе", custom_id="history", style=TextInputStyle.paragraph, min_length=1, max_length=300)
        ]
        if self.arg == "moderator":
            title = "Набор на должность модератора"
        else:
            title = "Набор на должность ведущего"
        super().__init__(title=title, components=components, custom_id="recruitementModal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        if self.arg == 'moderator':
            if for_moderator == False:
                await response.send_message("⛔ Сейчас набор на модератора закрыт!", ephemeral=True)
            elif for_moderator:
                name = interaction.text_values["name"]
                opt = interaction.text_values["opt"]
                history = interaction.text_values["history"]
                age = interaction.text_values["age"]
                embed = disnake.Embed(title="Заявка отправлена!", color=0x2ecc71)
                embed.description = f"{interaction.author.mention}, Благодарим вас за **заявку**! " \
                                    f"Если вы нам **подходите**, администрация **свяжется** с вами в ближайшее время. Ваш лс **обязательно** должен быть открыт!"
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                channel = interaction.guild.get_channel(859554058226237480)
                embed1 = disnake.Embed(title=f"Заявка на должность **{self.arg}**",
                                       description=f'От {interaction.author.mention}')
                embed1.add_field(name='Имя', value=name)
                embed1.add_field(name='Возраст', value=f"{age} лет")
                embed1.add_field(name='Опыт', value=opt)
                embed1.add_field(name='О нем', value=history)
                await channel.send(embed=embed1)
        else:
            if for_eventer == False:
                await interaction.response.send_message("⛔ Сейчас набор на ведущего закрыт!", ephemeral=True)
            elif for_eventer:
                name = interaction.text_values["name"]
                opt = interaction.text_values["opt"]
                history = interaction.text_values["history"]
                age = interaction.text_values["age"]
                embed = disnake.Embed(title="Заявка отправлена!", color = 0x2ecc71)
                embed.description = f"{interaction.author.mention}, Благодарим вас за **заявку**! " \
                                    f"Если вы нам **подходите**, администрация **свяжется** с вами в ближайшее время. Ваш лс **обязательно** должен быть открыт!"
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                channel = interaction.guild.get_channel(859554058226237480)
                embed1 = disnake.Embed(title=f"Заявка на должность **{self.arg}**", description=f'От {interaction.author.mention}')
                embed1.add_field(name='Имя', value=name)
                embed1.add_field(name='Возраст', value=f"{age} лет")
                embed1.add_field(name='Опыт', value=opt)
                embed1.add_field(name='О нем', value=history)
                await channel.send(embed=embed1)


class RecruitementSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Модератор", value="moderator", description="Модератор сервера"),
            disnake.SelectOption(label="Ведущий", value="eventsmod", description="Ведущий мероприятий"),
        ]
        super().__init__(
            placeholder="Выбери желаемую роль", options=options, min_values=0, max_values=1, custom_id="recruitement"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(RecruitementModal(interaction.values[0]))


class Recruitement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.slash_command(name='заявка', description='Подать заявку на модератора/ведущего')
    async def recruitment(self, interaction):
        view = disnake.ui.View()
        view.add_item(RecruitementSelect())
        # Тут можно добавть эмбед с описанием ролей
        if interaction.user.id in blacklist:
            embed = disnake.Embed(title="Ошибка", color = 0xe74c3c)
            embed.description = f"{interaction.author.mention}, Вы находитесь в ЧС администрации!"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral = True)
        else:
            embed = disnake.Embed(title="Подать заявку")
            embed.description = f"{interaction.author.mention}, Вы можете подать **заявку на должность**!" \
                    """\nПочему вам могут **отказать**: 
            1) Нетерпеливость (просьбы рассмотреть заявку и т.п.)
            2) Неадекватное поведение (как на сервере, так и на форуме)
            3) Недавние нарушения
            4) Неинформативная заявка
            5) Заявка написана неграмотно
            6) Флуд заявками
            7) С момента прошлого отказа не прошло месяца
            8) Недостоверная информация в заявке
            9) На сервере менее 72 часов"""
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral = True, view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitementSelect())
        self.bot.add_view(view,
                          message_id=...)  # Вставить ID сообщения, которое отправится после использования с команда !recruit


def setup(bot):
    bot.add_cog(Recruitement(bot))

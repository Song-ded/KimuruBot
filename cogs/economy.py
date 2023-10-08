import disnake
from disnake.ext import commands
from disnake.ui import View, Button

from utils.embeds import construct_basic_embed, construct_error_not_enough_embed, construct_error_negative_value_embed, construct_error_command_is_active

from utils.wheelgame import (
    get_multiplier,
    construct_wheel_embed,
    spin_wheel,
    initialize_multipliers,
    get_direction,
    MULTIPLIERS,
)

from utils.blackjk import (
    Hand,
    Deck,
    check_for_blackjack,
    show_blackjack_results,
    player_is_over,
    cards_emoji_representation,
    create_deck,
    deal_starting_cards,
    create_blackjack_embed,
    create_final_view,
    maybe_blackjack_cards,
    create_game_start_blackjack_embed,
    create_button,
    ViewAuthorCheck,
)

import random
import datetime
from utils.databases import UsersDataBase

##############################################################

class DuelEndEng(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(
        label="Дуэль",
        style=disnake.ButtonStyle.red,
        disabled=True,
    )
    async def duel_start(self, button: disnake.ui.View, interaction):
        pass


class DuelStartEng(disnake.ui.View):
    def __init__(self, author: disnake.User, bet: int, users_dict: dict):
        self.author = author
        self.bet = bet
        self.db = UsersDataBase()
        self.users_dict = users_dict
        super().__init__()


    async def interaction_check(self, interaction) -> bool:
        blnc = await self.db.get_user(interaction.user)
        if interaction.user == self.author:
            return False
        if blnc[1] < self.bet:
            return False
        else:
            return True

    @disnake.ui.button(
        label="Дуэль",
        style=disnake.ButtonStyle.red,
        disabled=False,
    )
    async def duel_start(self, button: disnake.ui.Button, interaction):
        author = self.author
        user = interaction.user
        who_win = random.choice([author, user])
        balance = await self.db.get_user(user)
        if balance[1] < self.bet:
            await interaction.message.edit(view=DuelEndEng())
            embed=construct_error_not_enough_embed(
                interaction.user.display_avatar,
                f"на балансе {balance[1]}",
            )
            return await interaction.response.send_message(embed=embed)
        balance = await self.db.get_user(author)
        if balance[1] < self.bet:
            await interaction.message.edit(view=DuelEndEng())
            embed=construct_error_not_enough_embed(
                interaction.user.display_avatar,
                f"на балансе {balance[1]}",
            )
            return await interaction.response.send_message(embed=embed)
        if who_win == author:
            losed = user
        else:
            losed = author
        embed = disnake.Embed(
            title=f"Дуэль",
            description=f"В дуэли побеждает {who_win.mention} и зарабатывает {self.bet}",
			color = 0xffffff,
        )
        await self.db.update_money(who_win, int(self.bet), 0)
        await self.db.update_money(losed, -abs(int(self.bet)), 0)
        msg = await self.db.get_user(who_win)
        embed.set_footer(text=f"Ваш баланс: {msg[1]}",icon_url=who_win.display_avatar)
        users_dict = self.users_dict
        if author.id in users_dict:
            users_dict.pop(author.id)
        if user.id in users_dict:
            users_dict.pop(user.id)
        await interaction.message.edit(embed=embed, view=DuelEndEng())
        return users_dict

################################

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
        self.users = dict()
        self.users_2 = dict()


    @commands.slash_command(
        name="дуэль",
        description="Сыграть дуэль с пользователем",
    )
    async def __duel(self, interaction, bet: int):
        if bet <= 0:
            await interaction.response.send_message("больше 0 поставь ставку")
        balance = await self.db.get_user(interaction.user)
        if balance[1] < bet:
            await interaction.response.send_message("у тебя нету денег")
        timestamp = datetime.datetime.now().timestamp()
        user = self.users_2.get(interaction.user.id, None)
        if user is None:
            self.users_2.update({interaction.user.id: timestamp})
        if user is not None:
            if timestamp - user < 120:
                return await interaction.send(
                    embed=construct_error_command_is_active(
                        interaction.user.display_avatar,
                    )
                )
        embed = disnake.Embed(
            title=f"Дуэль",
            description=f"{interaction.user.mention} запустил дуэль на **{bet}** ",
			color = 0xffffff,
        )

        await interaction.response.send_message(embed=embed, view=DuelStartEng(interaction.user, bet, self.users_2))
        if type(users_2) == dict:
            self.users_2 = users_2


    @commands.cooldown(1, 10800, commands.BucketType.user)
    @commands.slash_command(name='бонус', description='Получить награду в виде денег')
    async def timely(self, interaction):
        amount = random.randint(300, 650)
        embed = construct_basic_embed(
            f"{interaction.application_command.name} :hourglass:",
            f"На ваш счет были зачислены средства: " f"+__**{amount}**__ :coin:",
            f"команду использовал {interaction.user}",
            interaction.user.display_avatar,
            interaction.guild.id,
        )
        await self.db.update_money(interaction.user, amount, 0)
        await interaction.response.send_message(embed=embed)

    #@commands.Cog.listener()
    #async def on_slash_command_error(interaction, error):
       # if isinstance(error, commands.CommandOnCooldown):
         #   retry_after = str(datetime.timedelta(seconds=error.retry_after)).split('.')[0]
           # await interaction.response.send_message(f'**Вы устали, повторите попытку через {retry_after}**')
#
	
    @commands.slash_command(name='баланс', description='Посмотреть баланс')
    async def balance(self, interaction, member: disnake.Member = None):
        await self.db.create_table()
        if not member:
            member = interaction.author
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        embed = disnake.Embed(title=f'Баланс пользователя - {member}', color = 0xffffff)
        embed.add_field(name='🪙 Деньги', value=f'```{user[1]}```', inline = True)
        embed.add_field(name='💎 Премиум', value=f'```{round(user[2], 1)}```', inline = True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='курс', description='Посмотреть курс премиума')
    async def cccurs(self, interaction):
        await self.db.create_table4()
        await self.db.add_ccurs()
        curs = await self.db.get_ccurs()
        if curs[0] < 1000:
            await self.db.update_curs((-curs[0]) + 1000, 0)
        curs = await self.db.get_ccurs()
        embed = construct_basic_embed(
            f"{interaction.application_command.name}",
            f"{interaction.author.mention} сейчас курс :gem: состовляет 1:gem:к{curs[0]}:coin:",
            f"команду использовал {interaction.user}",
            interaction.user.display_avatar,
            interaction.guild.id,
        )
        await interaction.response.send_message(embed=embed)


    @commands.slash_command(name='обмен', description='Обменять деньги на премиум')
    async def exchange(self, interaction, amount: int, exchange=commands.Param(choices=['деньги', 'премиум'])):
        member = interaction.author
        await self.db.create_table()
        await self.db.create_table4()
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        curs = await self.db.get_ccurs()
        if exchange == 'деньги':
            if curs[0] < 1000:
                await self.db.update_curs((-curs[0]) + 1000, 0)
            curs = await self.db.get_ccurs()
            perm = amount * curs[0]
            if amount <= user[2]:
                await self.db.update_money(member, perm, (-amount))
                a = curs[0]/5 * random.randint(5, 10)
                await self.db.update_curs(random.randint(1, a), 0)
                embed = construct_basic_embed(
                    f"{interaction.application_command.name}",
                    f"{interaction.author.mention} обменял {amount}:gem: на {perm}:coin:",
                    f"команду использовал {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed=construct_error_not_enough_embed(
                    interaction.user.display_avatar,
                    f"на балансе {user[2]}",
                )
                await interaction.response.send_message(embed=embed)
        elif exchange=='премиум':
            if curs[0] < 1000:
                await self.db.update_curs((-curs[0]) + 1000, 0)
            curs = await self.db.get_ccurs()
            perm = amount / curs[0]
            if amount <= user[1]:
                if amount <= user[1]:
                    await self.db.update_money(member, (-amount), round(perm, 1)) # деньги                
                    a = curs[0] * random.randint(10, 30)
                    await self.db.update_curs(-abs(random.randint(0, a)), 0)                   
                    embed = construct_basic_embed(
                        f"{interaction.application_command.name}",
                        f"{interaction.author.mention} обменял {amount}:coin: на {round(perm, 1)}:gem:",
                        f"команду использовал {interaction.user}",
                        interaction.user.display_avatar,
                        interaction.guild.id,
                    )
                    await interaction.response.send_message(embed=embed)
                else:
                    embed=construct_error_not_enough_embed(
                        interaction.user.display_avatar,
                        f"на балансе {user[1]}",
                    )
                    await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='выдать', description='Выдать деньги пользователю')
    async def give(self, interaction, member: disnake.Member,
                   amount: int, arg=commands.Param(choices=['деньги', 'премиум'])):
        await self.db.create_table()
        await self.db.add_user(member)
        if arg == 'деньги':
            int(amount)
            await self.db.update_money(member, amount, 0)
            embed = construct_basic_embed(
                f"{interaction.application_command.name}",
                f"{interaction.author.mention} выдал: " f"+__**{amount}**__ :coin: пользователю {member.mention}",
                f"команду использовал {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        else:
            await self.db.update_money(member, 0, amount)
            embed = construct_basic_embed(
                f"{interaction.application_command.name}",
                f"{interaction.author.mention} выдал: " f"+__**{amount}**__ :gem: пользователю {member.mention}",
                f"команду использовал {interaction.user}",
                interaction.user.display_avatar,
                interaction.guild.id,
            )
        await interaction.response.send_message(embed=embed)


    @commands.slash_command(name='дать', description='Передать деньги пользователю')
    async def give_user(self, interaction, member: disnake.Member,
                   amount: float, arg=commands.Param(choices=['деньги', 'премиум'])):
        await self.db.create_table()
        await self.db.add_user(member)
        await self.db.add_user(interaction.user)
        user = await self.db.get_user(interaction.user)
        if amount <= 0:
            embed=construct_error_negative_value_embed(
                self.bot.user.avatar.url,
                int(amount),
            )
            await interaction.response.send_message(embed=embed)
            return
        if arg == 'деньги':
            if user[1] >= int(amount):
                int(amount)
                await self.db.update_money(member, int(amount), 0)
                await self.db.update_money(interaction.user, -abs(int(amount)), 0)
                embed = construct_basic_embed(
                    f"{interaction.application_command.name}",
                    f"{interaction.author.mention} перевел {amount}:coin: пользователю {member.mention}",
                    f"команду использовал {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed=construct_error_not_enough_embed(
                    interaction.user.display_avatar,
                    f"на балансе {user[1]}",
                )
                await interaction.response.send_message(embed=embed)
        else:
            if user[2] >= amount:
                await self.db.update_money(member, 0, amount)
                await self.db.update_money(interaction.user, 0, -abs(amount))
                embed = construct_basic_embed(
                    f"{interaction.application_command.name}",
                    f"{interaction.author.mention} перевел {amount}:gem: пользователю {member.mention}",
                    f"команду использовал {interaction.user}",
                    interaction.user.display_avatar,
                    interaction.guild.id,
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed=construct_error_not_enough_embed(
                    interaction.user.display_avatar,
                    f"на балансе {user[2]}",
                )
                await interaction.response.send_message(embed=embed)

    def get_multiplier(multipliers: list, index: int) -> int:
        return multipliers[index]

    @commands.slash_command(name="колесо",description="казино")
    async def __wheel(
            self,
            interaction,
            bet: int
    ):
        if bet <= 0:
            return await interaction.response.send_message(
                embed=construct_error_negative_value_embed(
                    self.bot.user.avatar.url,
                    bet,
                )
            )
        balance = await self.db.get_user(interaction.user)
        if balance[1] < bet:
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    interaction.user.display_avatar,
                    f"на балансе {balance[1]}",
                )
            )
        await self.db.update_money(interaction.author, int(-bet), 0)
        multipliers = [random.choice(MULTIPLIERS) for i in range(8)]
        wheel_number = random.randint(0, 7)
        bet_multiplier = get_multiplier(multipliers, wheel_number)
        await self.db.update_money(interaction.author, (int(bet * bet_multiplier)), 0)
        balance = await self.db.get_user(interaction.user)
        await interaction.response.send_message(
            embed=construct_wheel_embed(
                interaction.application_command.name.capitalize(),
                multipliers,
                get_direction(wheel_number),
                f"на балансе {balance1[1]}/{balance[1]}",
                interaction.user.display_avatar,
            )
        )

    @commands.slash_command(name="блекджек", description="Сыграть в блекджек")
    async def blackjack(self, interaction, bet: int):
        if bet <= 0:
            embed=construct_error_negative_value_embed(
                self.bot.user.avatar.url,
                bet,
            )
        balance = await self.db.get_user(interaction.user)
        if balance[1] < bet:
            return await interaction.response.send_message(
                embed=construct_error_not_enough_embed(
                    interaction.user.display_avatar,
                    f"на балансе {balance[1]}",
                )
            )
        global player
        player = interaction.user
        deck = create_deck()
        player_hand = Hand()
        dealer_hand = Hand(dealer=True)
        deal_starting_cards(player_hand, dealer_hand, deck)
        global turn
        turn = 1
        timestamp = datetime.datetime.now().timestamp()
        user = self.users.get(interaction.user.id, None)
        if user is None:
            self.users.update({interaction.user.id: timestamp})
        if user is not None:
            if timestamp - user < 120:
                return await interaction.send(
                    embed=construct_error_command_is_active(
                        interaction.user.display_avatar,
                    )
                )

        async def hit_callback(interaction):
            global turn
            turn += 1
            player_hand.add_card(deck.deal())
            if player_is_over(player_hand):
                await self.db.update_money(interaction.user, -bet, 0)
                balance = await self.db.get_user(interaction.user)
                msg = "Ваш баланс: "
                win = "победил"
                lost = "проиграл"
                embed = create_blackjack_embed(
                    self.bot,
                    f"{self.bot.user.mention} {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance[1]}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id,
                )
                view = create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.message.edit(embed=embed, view=view)
            else:
                turn_msg = "Ход"
                embed = create_game_start_blackjack_embed(
                    self.bot,
                    f"{turn_msg} {turn}",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                await interaction.message.edit(embed=embed)

        async def stand_callback(interaction):
            global turn
            turn += 1
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal())
                if player_is_over(dealer_hand):
                    update_user_balance(interaction.guild.id, interaction.user.id, bet)
                    balance = await self.db.get_user(interaction.user)
                    msg = "Ваш баланс: "
                    win = "победил"
                    embed = create_blackjack_embed(
                        self.bot,
                        f"**{interaction.user.mention}** {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance[1]}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id,
                    )
                    view = create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)
            if 17 <= dealer_hand.get_value() <= 21:
                if dealer_hand.get_value() > player_hand.get_value():
                    await self.db.update_money(interaction.user, -bet, 0)
                    balance = await self.db.get_user(interaction.user)
                    msg = "Ваш баланс: "
                    win = "победил"
                    lost = "проиграл"
                    embed = create_blackjack_embed(
                        self.bot,
                        f"{self.bot.user.mention} {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance[1]}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id,
                    )
                    view = create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)
                elif dealer_hand.get_value() == player_hand.get_value():
                    draw = "Ничья"
                    embed = create_blackjack_embed(
                        self.bot,
                        f"**{draw}**",
                        player_hand,
                        dealer_hand,
                        guild_id=interaction.guild.id,
                    )
                    view = create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)
                else:
                    await self.db.update_money(interaction.user, bet, 0)
                    balance = await self.db.get_user(interaction.user)
                    msg = "Ваш баланс: "
                    win = "победил"
                    lost = "проиграл"
                    embed = create_blackjack_embed(
                        self.bot,
                        f"**{interaction.user.mention}** {win}",
                        player_hand,
                        dealer_hand,
                        f"{msg} {balance[1]}",
                        interaction.user.display_avatar,
                        guild_id=interaction.guild.id,
                    )
                    view = create_final_view(interaction.guild.id)
                    self.users.pop(interaction.user.id)
                    await interaction.message.edit(embed=embed, view=view)

        async def dealer_blackjack_callback(interaction):
            if check_for_blackjack(dealer_hand):
                draw = "Ничья"
                embed = create_blackjack_embed(
                    self.bot,
                    f"**{draw}**",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                view = create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.message.edit(embed=embed, view=view)
            else:
                await self.db.update_money(interaction.user, int(bet * 1.5), 0)
                balance = await self.db.get_user(interaction.user)
                msg = "Ваш баланс: "
                win = "победил"
                lost = "проиграл"
                embed = create_blackjack_embed(
                    self.bot,
                    f"**{interaction.user.mention}** {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance[1]}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id,
                )
                view = create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.message.edit(embed=embed, view=view)

        async def one_to_one_callback(interaction):
            await self.db.update_money(interaction.user, bet, 0)
            balance = await self.db.get_user(interaction.user)
            msg = "Ваш баланс: "
            one_to_one_msg = "берет 1:1"
            embed = create_blackjack_embed(
                self.bot,
                f"**{interaction.user.mention}** {one_to_one_msg}",
                player_hand,
                dealer_hand,
                f"{msg} {balance[1]}",
                interaction.user.display_avatar,
                guild_id=interaction.guild.id,
            )
            view = create_final_view(interaction.guild.id)
            self.users.pop(interaction.user.id)
            await interaction.message.edit(embed=embed, view=view)

        if check_for_blackjack(player_hand):
            if str(dealer_hand.cards[1]) in maybe_blackjack_cards:
                dealer_blackjack = create_button(
                    "Blackjack", dealer_blackjack_callback, False
                )
                one_to_one = create_button("1:1", one_to_one_callback, False)
                view = ViewAuthorCheck(interaction.user)
                view.add_item(dealer_blackjack)
                view.add_item(one_to_one)
                turn_msg = get_msg_from_locale_by_key(interaction.guild.id, "turn")
                embed = create_game_start_blackjack_embed(
                    self.bot,
                    f"{turn_msg} {turn}",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await self.db.update_money(interaction.user, int(bet*1.5), 0)
                balance = await self.db.get_user(interaction.user)
                msg = "Ваш баланс: "
                win = "победил"
                lost = "проиграл"
                embed = create_blackjack_embed(
                    self.bot,
                    f"**{interaction.user.mention}** {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance[1]}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id,
                )
                view = create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.response.send_message(embed=embed, view=view)
        else:
            if check_for_blackjack(dealer_hand):
                await self.db.update_money(interaction.user, -bet, 0)
                balance = await self.db.get_user(interaction.user)
                msg = "Ваш баланс: "
                win = "победил"
                lost = "проиграл"
                embed = create_blackjack_embed(
                    self.bot,
                    f"{self.bot.user.mention} {win}",
                    player_hand,
                    dealer_hand,
                    f"{msg} {balance[1]}",
                    interaction.user.display_avatar,
                    guild_id=interaction.guild.id,
                )
                view = create_final_view(interaction.guild.id)
                self.users.pop(interaction.user.id)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                hit_msg = "Еще"
                stand_msg = "Хватит"
                hit = create_button(hit_msg, hit_callback, False)
                stand = create_button(stand_msg, stand_callback, False)
                view = ViewAuthorCheck(interaction.user)
                view.add_item(hit)
                view.add_item(stand)
                turn_msg = "Ход"
                embed = create_game_start_blackjack_embed(
                    self.bot,
                    f"{turn_msg} {turn}",
                    player_hand,
                    dealer_hand,
                    guild_id=interaction.guild.id,
                )
                await interaction.response.send_message(embed=embed, view=view)


    @commands.slash_command(name='топ_по_валюте', description='Посмотреть топ пользователей по валюте')
    async def top_money(self, interaction):
        await self.db.create_table()
        top = await self.db.get_top()
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
                text += f'**{n}.** {string1} - {user[1]} :coin:\n'
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

def setup(bot):
    bot.add_cog(Economy(bot))

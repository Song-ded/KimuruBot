import random

import disnake
from disnake.ui import Button, View


def create_button(label: str, callback=False, disabled: bool = False):
    button = Button(label=label, style=disnake.ButtonStyle.secondary, disabled=disabled)
    if callback is not False:
        button.callback = callback
    return button

maybe_blackjack_cards = [
    "10 of Clubs",
    "J of Clubs",
    "Q of Clubs",
    "K of Clubs",
    "A of Spades",
    "10 of Diamonds",
    "J of Diamonds",
    "Q of Diamonds",
    "K of Diamonds",
    "A of Diamonds",
]

cards_emoji_representation = {
    "hidden": 1160643541941358644,
    "A of Diamonds":1160643559846838404,
    "2 of Diamonds":1160643554717208608,
    "3 of Diamonds":1160643552162881597,
    "4 of Diamonds":1160643568029937786,
    "5 of Diamonds":1160643564871626832,
    "6 of Diamonds":1160643572605931671,
    "7 of Diamonds":1160643573700636734,
    "8 of Diamonds":1160643562560552990,
    "9 of Diamonds":1160643550791336006,
    "10 of Diamonds":1160643571255345262,
    "J of Diamonds":1160643546894835903,
    "Q of Diamonds":1160643545208729733,
    "K of Diamonds":1160643549407215787,
    "A of Clubs":1160643609964576818,
    "2 of Clubs":1160643558030708777,
    "3 of Clubs":1160643633096183918,
    "4 of Clubs":1160643618495791144,
    "5 of Clubs":1160643614230200484,
    "6 of Clubs":1160643628922847432,
    "7 of Clubs":1160643627534524578,
    "8 of Clubs":1160643612456013915,
    "9 of Clubs":1160643623726096554,
    "10 of Clubs":1160643631389094039,
    "J of Clubs":1160643617061355601,
    "Q of Clubs":1160643626058121387,
    "K of Clubs":1160643620228055200,
}


def check_for_blackjack(hand) -> bool:
    if hand.get_value() == 21:
        return True
    else:
        return False


def player_is_over(player_hand):
    return player_hand.get_value() > 21


def show_blackjack_results(player_has_blackjack, dealer_has_blackjack):
    if player_has_blackjack and dealer_has_blackjack:
        print("Both players have blackjack! Draw!")

    elif player_has_blackjack:
        print("You have blackjack! You win!")

    elif dealer_has_blackjack:
        print("Dealer has blackjack! Dealer wins!")


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return " of ".join((self.value, self.suit))


class Deck:
    def __init__(self):
        self.cards = [
            Card(s, v)
            for s in ["Clubs", "Diamonds"]
            for v in [
                "A",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "J",
                "Q",
                "K",
                "A",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "J",
                "Q",
                "K",
                "A",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "J",
                "Q",
                "K",
                "A",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "J",
                "Q",
                "K",
            ]
        ]

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)


class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):
        if self.dealer:
            return ["hidden", self.cards[1]]
        else:
            for card in self.cards:
                print(card)
            print(self.get_value())


def create_deck() -> Deck:
    deck = Deck()
    deck.shuffle()
    return deck


def deal_starting_cards(player_hand: Hand, dealer_hand: Hand, deck: Deck) -> None:
    for i in range(2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())


def get_hand_cards(bot, hand: Hand) -> str:
    field_value = " "
    for card in hand.cards:
        card = str(card)
        if card in cards_emoji_representation:
            field_value += f"{bot.get_emoji(cards_emoji_representation[card])} "
        else:
            field_value += f"{card} "
    return field_value


def get_hand_hidden_cards(bot, hand: Hand) -> str:
    field_value = " "
    for card in hand.display():
        card = str(card)
        if card in cards_emoji_representation:
            field_value += f"{bot.get_emoji(cards_emoji_representation[card])} "
        else:
            field_value += f"{card} "
    return field_value


def create_blackjack_embed(
    bot,
    state_of_game: str,
    player_hand: Hand,
    dealer_hand: Hand,
    footer_text: str = None,
    footer_url: str = None,
    guild_id: int = None,
) -> disnake.Embed:
    player_hand_msg = "Ваша рука"
    dealer_hand_msg = "Руки диллера"
    value_msg = "Ценность"
    title = "Блэкджек"
    embed = disnake.Embed(
        title=title, description=state_of_game, color = 0xffffff
    )
    player_hand_field_value = get_hand_cards(bot, player_hand)
    dealer_hand_field_value = get_hand_cards(bot, dealer_hand)
    embed.add_field(
        name=f"{player_hand_msg}",
        value=f"{player_hand_field_value}\n"
        f"{value_msg} **{player_hand.get_value()}**",
        inline=True,
    )
    embed.add_field(
        name=f"{dealer_hand_msg}",
        value=f"{dealer_hand_field_value}\n"
        f"{value_msg} **{dealer_hand.get_value()}**",
        inline=True,
    )
    if footer_text is not None and footer_url is not None:
        embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed


def create_game_start_blackjack_embed(
    bot,
    state_of_game: str,
    player_hand: Hand,
    dealer_hand: Hand,
    footer_text: str = None,
    footer_url: str = None,
    guild_id: int = None,
) -> disnake.Embed:
    player_hand_msg = "Ваша рука"
    dealer_hand_msg = "Руки диллера"
    value_msg = "Ценность"
    title = "Блэкджек"
    embed = disnake.Embed(title=title, description=state_of_game, color = 0xffffff)
    player_hand_field_value = get_hand_cards(bot, player_hand)
    dealer_hand_field_value = get_hand_hidden_cards(bot, dealer_hand)
    embed.add_field(
        name=f"{player_hand_msg}",
        value=f"{player_hand_field_value}\n"
        f"{value_msg} **{player_hand.get_value()}**",
        inline=True,
    )
    second_dealer_card = dealer_hand.cards[1]
    if second_dealer_card.value in ["J", "K", "Q"]:
        second_dealer_card = 10
    elif second_dealer_card.value == "A":
        second_dealer_card = 11
    else:
        second_dealer_card = second_dealer_card.value
    embed.add_field(
        name=f"{dealer_hand_msg}",
        value=f"{dealer_hand_field_value}\n{value_msg} **{second_dealer_card}**",
        inline=True,
    )
    if footer_text is not None and footer_url is not None:
        embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed


def create_final_view(guild_id: int):
    hit_msg = "Еще"
    stand_msg = "Хватит"
    hit = create_button(hit_msg, False, True)
    stand = create_button(stand_msg, False, True)
    view = View()
    view.add_item(hit)
    view.add_item(stand)
    return view

class ViewAuthorCheck(View):
    def __init__(self, author: disnake.user):
        self.author = author
        super().__init__()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.author:
            return False
        return True
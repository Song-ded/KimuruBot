import disnake
from disnake.ext import commands

white = 0xffffff

def construct_basic_embed(
    name: str, value: str, footer_text: str, footer_url: str, guild_id: int
) -> disnake.Embed:
    try:
        name = name
        name = name.capitalize()
    except Exception as error:
        name = name
        name = name.capitalize()
    name = name.replace("_", " ")
    embed = disnake.Embed(color=0xffffff)
    embed.add_field(name=name, value=value)
    embed.set_footer(text=footer_text, icon_url=footer_url)
    return embed

def construct_error_embed(description: str) -> disnake.Embed:
    embed = disnake.Embed(color=0xffffff, description=description)
    return embed

def construct_error_not_enough_embed(icon: str, footer_text) -> disnake.Embed:
    embed = construct_error_embed("У вас недостаточно денег для выполнения команды.")
    embed.set_footer(icon_url=icon, text=footer_text)
    return embed

def construct_error_negative_value_embed(icon: str, value) -> disnake.Embed:
    embed = construct_error_embed("Бот прекратил процесс исполнения данной команды по причине: __**не положительное или неправильное значение**__\nПроцесс выполнения вашей команды был остановлен.")
    embed.set_footer(
        icon_url=icon,
        text=f"error: NOT POSITIVE/NOT INT VALUE\nvalue: {value}\nstatus-code: #K143",
    )
    return embed

def construct_error_command_is_active(icon: str) -> disnake.Embed:
    embed = construct_error_embed("Бот прекратил процесс исполнения данной команды по причине: __**процесс исполнения уже активен**__\nПроцесс выполнения вашей команды был остановлен.")
    embed.set_footer(
        icon_url=icon,
        text=f"error: command_is_active\nstatus-code: #K306 ",
    )
    return embed

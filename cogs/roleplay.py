import random
from utils.storage import (
    respect_gifs,
    idk_gifs,
    hug_gifs,
    kiss_gifs,
    punch_gifs,
    cry_gifs,
    bite_gifs,
    spank_gifs,
    five_gifs,
    pat_gifs,
    lick_gifs,
)

import disnake
from disnake.ext import commands


class Reaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='шлепнуть', description='Шлепнуть пользователя')
    async def spank(self, interaction, member: disnake.Member):
        embed = disnake.Embed(color=member.color, title="Эмоция: шлепнуть")
        embed.description = f"{interaction.author.mention} шлепнул {member.mention}"
        url = (random.choice(spank_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='пять', description='Дать пять')
    async def five(self, interaction, member: disnake.Member):
        embed = disnake.Embed(title="Эмоция: дать пять")
        embed.description = f"{interaction.author.mention} дал пять {member.mention}"
        url = (random.choice(five_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='расстроиться', description='Расстроиться')
    async def cry(self, interaction):
        embed = disnake.Embed(title="Эмоция: расстроиться")
        embed.description = f"{interaction.author.mention} расстроился"
        url = (random.choice(cry_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='не_знать', description='Не знаю')
    async def idk(self, interaction):
        embed = disnake.Embed(title="Эмоция: не знать")
        embed.description = f"{interaction.author.mention} не знает"
        url = (random.choice(idk_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='респект', description='Выразить респект')
    async def respect(self, interaction, member: disnake.Member = None):
        embed = disnake.Embed(title="Эмоция: респект")
        if member == None:
            embed.description = f"{interaction.author.mention} выразил респект"
        else:
            embed.description = f"{interaction.author.mention} выразил респект {member.mention}"
        url = (random.choice(respect_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='погладить', description='Погладить пользователя')
    async def pat(self, interaction, member: disnake.Member):
        embed = disnake.Embed(color=member.color, title="Эмоция: погладить")
        embed.description = f"{interaction.author.mention} погладил {member.mention}"
        url = (random.choice(pat_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='лизнуть', description='Лизнуть пользователя')
    async def lick(self, interaction, member: disnake.Member):
        embed = disnake.Embed(color=member.color, title="Эмоция: лизнуть")
        embed.description = f"{interaction.author.mention} лизнул {member.mention}"
        url = (random.choice(lick_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='обнять', description='Обнять пользователя')
    async def hugh(self, interaction, member: disnake.Member):
        embed = disnake.Embed(color=member.color, title="Эмоция: обнять")
        embed.description = f"{interaction.author.mention} обнял {member.mention}"
        url = (random.choice(hug_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='ударить', description='Ударить пользователя')
    async def punch(self, interaction, member: disnake.Member):
        embed = disnake.Embed(color=member.color, title="Эмоция: ударить")
        embed.description = f"{interaction.author.mention} ударил {member.mention}"
        url = (random.choice(punch_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='поцеловать', description='Поцеловать пользователя')
    async def kiss(self, interaction, member: disnake.Member):
        embed = disnake.Embed(color=member.color, title="Эмоция: поцеловать")
        embed.description = f"{interaction.author.mention} поцеловал {member.mention}"
        url = (random.choice(kiss_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='кусать', description='Укусить пользователя')
    async def bite(self, interaction, member: disnake.Member):
        embed = disnake.Embed(color=member.color, title="Эмоция: укус")
        embed.description = f"{interaction.author.mention} укусил {member.mention}"
        url = (random.choice(bite_gifs))
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Reaction(bot))

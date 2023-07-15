import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='создать_мероприятие', description='Создать мероприятие')
    async def event(self, interaction, arg=commands.Param(choices=['Бункер', 'Настолки']), time=commands.Param(choices=['Через 30 минут', 'Через час', 'Через 2 часа'])):
        if time == 'Через 30 минут':
            clock = datetime.now() + timedelta(minutes=30)
        elif time == 'Через час':
            clock = datetime.now() + timedelta(minutes=60)
        elif time == 'Через 2 часа':
            clock = datetime.now() + timedelta(minutes=120)


        if arg == "Бункер":
            embed = disnake.Embed(title=f"Бункер - {clock.strftime('%H:%M')}",
                                  description="В игре ты получаешь уникального персонажа, которым постараешься доказать всем, что именно ты должен попасть в бункер, чтобы спастись! Ты должен быть готов к любым препятствиям. Остальные игроки, пытающиеся выжить, будут доказывать обратное... \n\n• **Канал мероприятия:** <#1129851362868469911>",
                                  color=0xe3e3e3)
            embed.set_author(name=f"Ведущий - {interaction.author}")
            embed.set_image(url="https://media.discordapp.net/attachments/720718813514956840/1129848883288215612/bunker.jpg?width=1228&height=663")
            embed.add_field(name="Участие", value="300🪙", inline=True)
            embed.add_field(name="Победа", value="1000🪙", inline=True)
            channel = interaction.guild.get_channel(997014623935012935)
            await channel.send(embed=embed)
        if arg == "Настолки":
            embed = disnake.Embed(title=f"Настолки - {clock.strftime('%H:%M')}",
                                  description="Настольные игры и стратегические игры для двух и более человек. Обязательно приходи с хорошим настроением. \n\n• **Канал мероприятия:** <#1129851362868469911>",
                                  color=0xe3e3e3)
            embed.set_author(name=f"Ведущий - {interaction.author}")
            embed.set_image(url="https://media.discordapp.net/attachments/720718813514956840/1129875958879498260/nastolki.jpg?width=1228&height=663")
            embed.add_field(name="Участие", value="300🪙", inline=True)
            embed.add_field(name="Победа", value="800🪙", inline=True)
            channel = interaction.guild.get_channel(997014623935012935)
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
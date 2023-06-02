import disnake
from disnake.ext import commands

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'option': '-vn'}
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='играть', description='Включить музыку')
    async def play(self, interaction, song_name: str):

        source = await disnake.FFmpegOpusAudio.from_probe(f"{song_name}.mp3", executable="C:/Users/Veter/OneDrive/Рабочий стол/bot/cogs/ffmpeg/ffmpeg.exe")
        disnake.voice_client.play(source)
        await interaction.user.voice.channel.connect(reconnect=True)


def setup(bot):
    bot.add_cog(Music(bot))
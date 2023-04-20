from youtube_dl import YoutubeDL

import disnake
from disnake.ext import commands

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(ctx, url, message):
        vc = ctx.message.user.voice.channel 

        with YoutubeDL(YDL_OPTIONS) as ydl:
            if 'https://' in url:
                info = ydl.extract_info(url, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entrise'][0]
        link = info['formats'][0]['url']

        vc.play(disnake.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=link, **FFMPEG_OPTIONS))


def setup(bot):
    bot.add_cog(Music(bot))
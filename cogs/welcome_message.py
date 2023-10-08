import disnake
from disnake.ext import commands, tasks

import numpy as np
import cv2

import asyncio
import datetime
from utils.databases import UsersDataBase
class Welcome_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()
        self.task.start()

    @tasks.loop(seconds=1.0)
    async def task(self):
        nowtime1 = str(datetime.datetime.now().time().strftime("%H.%M.%S"))
        if nowtime1 == "21.00.00":
            await self.db.clear_server_stats()


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if member.bot:
            return
        if member.id == "823726493967450132":
            await guild.ban(member, reason=None)
        channel = guild.system_channel
        embed = disnake.Embed(color = 0x2ecc71, title=f"Miko Family", description=f"{member.mention} Приветствуем тебя на сервере!")
        embed.set_footer(text=f"Miko Family", icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar)
        await channel.send(embed=embed)
        await self.db.create_table3()
        await self.db.joined()


    @commands.Cog.listener()
    async def on_member_leave(self, member):
        if member.bot:
            return
        await self.db.create_table3()
        await self.db.leaved()

    @commands.slash_command()
    async def serverstatstechcommand(self, interaction):
        await self.db.add_statsserver()

    @commands.slash_command()
    async def stats(self, interaction):
        await self.db.create_table3()
        stat = await self.db.get_serverstats()
        embed = disnake.Embed(color=0x2ecc71, title=f"Miko Family",
                              description=f"Статистика сервера за последнии 24 часа")
        embed.set_footer(text=f"Miko Family")
        if stat[0] == None:
            s1 = 0
        else:
            s1 = stat[0]
        if stat[1] == None:
            s2 = 0
        else:
            s2 = stat[1]
        embed.add_field(name='Зашли - ', value=s1)
        embed.add_field(name='Вышли - ', value=s2)
        embed.add_field(name='Профит - ', value=s1 - s2)
        member = interaction.user
        #embed.set_thumbnail(url=member.guild.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=False)

def setup(bot):
    bot.add_cog(Welcome_message(bot))
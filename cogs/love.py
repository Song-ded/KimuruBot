import disnake
from disnake.ext import commands
from utils.databases import UsersDataBase
from datetime import datetime

class Lovepy(commands.Cog):
	def __init__(self, bot):
	    self.bot = bot
	    self.db = UsersDataBase()
	
	@commands.cooldown(1, 6000, commands.BucketType.user)
	@commands.slash_command(name='письмо', description='Написать анонимное письмо человеку [Цена 5000]')
	async def anonim(self, interaction, member: disnake.Member, text: str):
		print("Anonim message")
		await self.db.create_table()
		await self.db.add_user(interaction.user)
		user = await self.db.get_user(interaction.user)
		if member == interaction.user:
			await interaction.response.send_message('Все в порядке, но.. Вы указали самого себя😢', ephemeral=True)
		elif member.bot:
			await interaction.response.send_message('Все в порядке, но.. Вы указали бота😢', ephemeral=True)
		elif len(text) > 80:
			await interaction.response.send_message('Все в порядке, но.. Вы написали слишком длинное письмо😢', ephemeral=True)
		else:
			if 5000 <= user[1]:
				print(f"member - {member}")
				print(f"author - {interaction.user}")
				print(f"text - {text}")
				print("-----------------")
				embed = disnake.Embed(title="Письмо✉️", description=text, color = 0xffffff)
				embed.set_thumbnail(url=member.display_avatar.url)
				try:
					await member.send(embed=embed)
					embed1 = disnake.Embed(title=f'Анонимное письмо - {member}', description="Письмо успешно отправлено!", color = 0x2ecc71)
					embed1.set_thumbnail(url=member.display_avatar.url)
					await interaction.response.send_message(embed=embed1, ephemeral=True)
					await self.db.update_money(interaction.user, -5000, 0)
				except:
					await interaction.response.send_message('Все в порядке, но.. У человека видимо закрыто ЛС😢', ephemeral=True)
			else:
				embed = disnake.Embed(title=f'Анонимное письмо - {member}', description="У вас не хватает денег!", color=0xe74c3c)
				embed.set_thumbnail(url=member.display_avatar.url)
				await interaction.response.send_message(embed=embed, ephemeral=True)


	#@commands.Cog.listener()
	#async def on_slash_command_error(ctx, error):
	#	if isinstance(error, commands.CommandOnCooldown):
	#		retry_after = str(datetime.timedelta(seconds=error.retry_after)).split('.')[0]
	#		await ctx.send(f'**Вы сможете отправить письмо через {retry_after}**')

def setup(bot):
	bot.add_cog(Lovepy(bot))
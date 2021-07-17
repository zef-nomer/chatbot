import discord
from discord.ext import commands


class name(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_


def setup(bot):
    bot.add_cog(name(bot))


'''
Образец Кога

class name(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	...


def setup(bot):
	bot.add_cog(name(bot))
'''
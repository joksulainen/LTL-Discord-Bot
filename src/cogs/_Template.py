import discord
import discord.ext.commands as extCommands
from discord import ApplicationContext, Option, slash_command

from LTLBot import LTLBot


class CogTemplate(extCommands.Cog, name=__name__):
    def __init__(self, bot: LTLBot):
        self.BOT = bot
        self.__cog_guild_ids__ = [bot.config.guild_id]


# Extension related functions
def setup(bot: LTLBot):
    bot.add_cog(CogTemplate(bot))

def teardown(bot: LTLBot):
    bot.remove_cog(__name__)

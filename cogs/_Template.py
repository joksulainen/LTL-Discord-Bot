import discord
from discord import ApplicationContext, Option, slash_command
import discord.ext.commands as extCommands

from handlers.config import config


class CTemplate(extCommands.Cog, name=__name__, guild_ids=[config.guild_id]):
    def __init__(self, bot: discord.Bot):
        self.BOT = bot


# Extension related functions
def setup(bot: discord.Bot):
    bot.add_cog(CTemplate(bot))

def teardown(bot: discord.Bot):
    bot.remove_cog(__name__)

import discord
from discord import ApplicationContext, Option, slash_command
import discord.ext.commands as extCommands

from config_handler import config


class CEventControl(extCommands.Cog, name=__name__, guild_ids=[config.guild_id]):
    def __init__(self, bot: discord.Bot):
        self.BOT = bot


    # Application commands
    @slash_command()
    async def event_hello_world(self, ctx: ApplicationContext):
        """Hello world!"""
        await ctx.respond("Hello world from the EventControl group!", ephemeral=True)


# Extension related functions
def setup(bot: discord.Bot):
    bot.add_cog(CEventControl(bot))

def teardown(bot: discord.Bot):
    bot.remove_cog(__name__)

import discord
from discord import ApplicationContext, Option, slash_command
import discord.ext.commands as extCommands

import handlers.config
from handlers.config import config
from permission_decorators import is_admin, is_moderator


class CUngrouped(extCommands.Cog, name=__name__, guild_ids=[config.guild_id]):
    def __init__(self, bot: discord.Bot):
        self.BOT = bot
    
    
    # Application commands
    @slash_command()
    async def hello_world(self, ctx: ApplicationContext):
        """Hello world!"""
        await ctx.respond("Hello world from the ungrouped group!", ephemeral=True)


# Extension related functions
def setup(bot: discord.Bot):
    bot.add_cog(CUngrouped(bot))

def teardown(bot: discord.Bot):
    bot.remove_cog(__name__)

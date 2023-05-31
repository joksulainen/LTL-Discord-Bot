import discord
from discord import ApplicationContext, Option, slash_command
import discord.ext.commands as extCommands

import config_handler
from config_handler import config
from permission_decorators import is_admin, is_moderator


class CUngrouped(extCommands.Cog, name=__name__, guild_ids=[config.guild_id]):
    def __init__(self, bot: discord.Bot):
        self.BOT = bot
    
    
    # Application commands
    @slash_command()
    @extCommands.is_owner()
    async def reload_config(self, ctx: ApplicationContext):
        """Reload config"""
        config_handler.reload_config()
        await ctx.respond("Config reloaded", ephemeral=True)


# Extension related functions
def setup(bot: discord.Bot):
    bot.add_cog(CUngrouped(bot))

def teardown(bot: discord.Bot):
    bot.remove_cog(__name__)

import discord
import discord.ext.commands as extCommands
import discord.ext.pages as extPages
from discord import ApplicationContext, Option, slash_command

from LTLBot import LTLBot


class CogUngrouped(extCommands.Cog, name=__name__):
    def __init__(self, bot: LTLBot):
        self.BOT = bot
        self.__cog_guild_ids__ = [bot.config.guild_id]
    
    
    # Application commands
    @slash_command(name="leaderboard")
    async def leaderboard(self, ctx: ApplicationContext):
        """View the leaderboard for the current or previous event, whichever is applicable"""
        # acknowledge command
        await ctx.defer()
        
        # acquire a copy of the leaderboard
        lb = self.BOT.persistence.leaderboard
        
        # respond with the leaderboard paginator
        await ctx.respond("Insert leaderboard here")


# Extension related functions
def setup(bot: LTLBot):
    bot.add_cog(CogUngrouped(bot))

def teardown(bot: LTLBot):
    bot.remove_cog(__name__)

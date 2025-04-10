import discord
import discord.ext.commands as extCommands
from discord import ApplicationContext, Option, slash_command, OptionChoice

from LTLBot import LTLBot
from utils import is_admin
from utils.json_wrappers import update_config


async def ac_permission(ctx: discord.AutocompleteContext):
    if not await ctx.bot.is_owner(ctx.interaction.user):
        return [OptionChoice("this command does nothing for you, go away", "")]
    options = [OptionChoice("None", "none"), OptionChoice("Administrator", "admin")]
    return options


class CogConfiguration(extCommands.Cog, name=__name__):
    def __init__(self, bot: LTLBot):
        self.BOT = bot
        self.__cog_guild_ids__ = [bot.config.guild_id]
    
    
    # Application commands
    GROUP = discord.SlashCommandGroup("config")
    
    
    PERMISSION_GROUP = GROUP.create_subgroup("permission", "Manage user permissions for bot")
    @PERMISSION_GROUP.command(name="set", options=[
        Option(discord.User, name="user"), Option(str, name="permission", autocomplete=ac_permission)
    ])
    @extCommands.is_owner()
    async def config_permission_set(self, ctx: ApplicationContext, user: discord.Member, permission: str):
        """Set user permission for bot"""
        output_str = ""
        match permission:
            case "admin":
                pass
            case "none" | _:
                pass
        await ctx.respond(output_str, ephemeral=True)
    
    @PERMISSION_GROUP.command(name="list", options=[])
    @is_admin()
    async def config_permission_list(self, ctx: ApplicationContext):
        """List users with permissions on the bot"""
        users = list()
        if self.BOT.owner_id is None:
            for id in self.BOT.owner_ids:
                users.append(f"<@{id}> - Owner")
        else:
            users.append(f"<@{self.BOT.owner_id}> - Owner")
        for id in self.BOT.config.admin_ids:
            users.append(f"<@{id}> - Admin")
        await ctx.respond("List of users with permission:\n{}".format("\n".join(users)), ephemeral=True)


# Extension related functions
def setup(bot: LTLBot):
    bot.add_cog(CogConfiguration(bot))

def teardown(bot: LTLBot):
    bot.remove_cog(__name__)

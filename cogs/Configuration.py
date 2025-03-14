import discord
import discord.ext.commands as extCommands
from discord import ApplicationContext, Option, slash_command, OptionChoice

from LTLBot import LTLBot
from utils import is_admin, is_moderator
from utils.json_wrappers import update_config


async def ac_permission(ctx: discord.AutocompleteContext):
    is_owner = await ctx.bot.is_owner(ctx.interaction.user)
    if (not (ctx.interaction.user.id in (ctx.bot).config.moderator_ids + (ctx.bot).config.admin_ids) and
        not is_owner):
        return [OptionChoice("this command does nothing for you, go away", "")]
    options = [OptionChoice("None", "none"), OptionChoice("Moderator", "mod")]
    if is_owner:
        options.append(OptionChoice("Administrator", "admin"))
    return options


class CogConfiguration(extCommands.Cog, name=__name__):
    def __init__(self, bot: LTLBot):
        self.BOT = bot
        self.__cog_guild_ids__ = [bot.config.guild_id]
    
    
    # Application commands
    GROUP = discord.SlashCommandGroup("config", "Base command")
    
    
    PERMISSION_GROUP = GROUP.create_subgroup("permission", "Manage user permissions for bot")
    @PERMISSION_GROUP.command(name="set", options=[
        Option(discord.User, name="user"), Option(str, name="permission", autocomplete=ac_permission)
    ])
    @is_admin()
    async def config_permission_set(self, ctx: ApplicationContext, user: discord.User, permission: str):
        """Set user permission for bot"""
        output_str = ""
        match permission:
            case "admin":
                pass
            case "mod":
                pass
            case "none" | _:
                pass
        await ctx.respond(output_str, ephemeral=True)
    
    @PERMISSION_GROUP.command(name="list", options=[])
    @is_moderator()
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
        for id in self.BOT.config.moderator_ids:
            users.append(f"<@{id}> - Moderator")
        await ctx.respond("List of users with permission:\n{}".format("\n".join(users)), ephemeral=True)


# Extension related functions
def setup(bot: LTLBot):
    bot.add_cog(CogConfiguration(bot))

def teardown(bot: LTLBot):
    bot.remove_cog(__name__)

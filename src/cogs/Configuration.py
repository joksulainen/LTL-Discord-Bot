import discord
import discord.ext.commands as extCommands
from discord import ApplicationContext, Option, slash_command, OptionChoice

from LTLBot import LTLBot
from utils import is_admin
from utils.json_wrappers import update_config


class CogConfiguration(extCommands.Cog, name=__name__):
    def __init__(self, bot: LTLBot):
        self.BOT = bot
        self.__cog_guild_ids__ = [bot.config.guild_id]
    
    
    # Application commands
    GROUP = discord.SlashCommandGroup("config")
    
    
    ADMIN_GROUP = GROUP.create_subgroup("admin", "Manage bot admins")
    
    @ADMIN_GROUP.command(name="add", options=[
        Option(discord.User, name="user", description="The user to give admin to")
    ])
    @extCommands.is_owner()
    async def config_admin_add(self, ctx: ApplicationContext, user: discord.User):
        """Give admin to a user"""
        if await self.BOT.is_owner(user):
            await ctx.respond("Can't make yourself (the owner) an admin", ephemeral=True)
            return
        admin_ids = self.BOT.config.admin_ids
        if user.id in admin_ids:
            await ctx.respond(f"{user.mention} already has admin", ephemeral=True)
            return
        admin_ids.append(user.id)
        update_config(self.BOT.config, admin_ids=admin_ids)
        await ctx.respond(f"Admin given to {user.mention}", ephemeral=True)
    
    @ADMIN_GROUP.command(name="remove" , options=[
        Option(discord.User, name="user", description="The user to remove admin from")
    ])
    @extCommands.is_owner()
    async def config_admin_remove(self, ctx: ApplicationContext, user: discord.User):
        """Remove admin from a user"""
        if await self.BOT.is_owner(user):
            await ctx.respond("Can't unmake yourself (the owner) an admin", ephemeral=True)
            return
        admin_ids = self.BOT.config.admin_ids
        if user.id not in admin_ids:
            await ctx.respond(f"{user.mention} doesn't have admin", ephemeral=True)
            return
        admin_ids.remove(user.id)
        update_config(self.BOT.config, admin_ids=admin_ids)
        await ctx.respond(f"Admin removed from {user.mention}", ephemeral=True)
    
    @ADMIN_GROUP.command(name="list", options=[])
    @is_admin()
    async def config_admin_list(self, ctx: ApplicationContext):
        """List users with admin permissions on the bot"""
        users = list()
        if self.BOT.owner_id is None:
            for id in self.BOT.owner_ids:
                users.append(f"<@{id}> - Owner")
        else:
            users.append(f"<@{self.BOT.owner_id}> - Owner")
        for id in self.BOT.config.admin_ids:
            users.append(f"<@{id}> - Admin")
        await ctx.respond("List of users with admin permission:\n{}".format("\n".join(users)), ephemeral=True)


# Extension related functions
def setup(bot: LTLBot):
    bot.add_cog(CogConfiguration(bot))

def teardown(bot: LTLBot):
    bot.remove_cog(__name__)

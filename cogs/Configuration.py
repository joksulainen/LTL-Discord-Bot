import discord
from discord import ApplicationContext, Option, slash_command
import discord.ext.commands as extCommands

import handlers.config
from handlers.config import CONFIG
from permission_decorators import is_admin


class CConfiguration(extCommands.Cog, name=__name__, guild_ids=[CONFIG.guild_id]):
    def __init__(self, bot: discord.Bot):
        self.BOT = bot
    
    
    # Application commands
    GROUP = discord.SlashCommandGroup("config", "Base command")
    
    @GROUP.command(name="reload")
    async def config_reload(self, ctx: ApplicationContext):
        """Reload config"""
        handlers.config.reload_config()
        await ctx.respond("Config reloaded", ephemeral=True)
    
    
    ADMIN_GROUP = GROUP.subgroup("admin", "Manage bot admins")
    @ADMIN_GROUP.command(name="add", options=[Option(discord.User, name="user")])
    @extCommands.is_owner()
    async def config_admin_add(self, ctx: ApplicationContext, user: discord.User):
        """Add a user as bot admin"""
        await ctx.respond(f"Admin add test ({user.id})", ephemeral=True)
    
    @ADMIN_GROUP.command(name="remove", options=[Option(discord.User, name="user")])
    @extCommands.is_owner()
    async def config_admin_remove(self, ctx: ApplicationContext, user: discord.User):
        """Remove a user as bot admin"""
        await ctx.respond(f"Admin remove test ({user.id})", ephemeral=True)
    
    
    MODERATOR_GROUP = GROUP.subgroup("moderator", "Manage bot moderators")
    @MODERATOR_GROUP.command(name="add", options=[Option(discord.User, name="user")])
    @is_admin()
    async def config_moderator_add(self, ctx: ApplicationContext, user: discord.User):
        """Add a user as bot moderator"""
        await ctx.respond(f"Moderator add test ({user.id})", ephemeral=True)
    
    @MODERATOR_GROUP.command(name="remove", options=[Option(discord.User, name="user")])
    @is_admin()
    async def config_moderator_remove(self, ctx: ApplicationContext, user: discord.User):
        """Remove a user as bot moderator"""
        await ctx.respond(f"Moderator remove test ({user.id})", ephemeral=True)


# Extension related functions
def setup(bot: discord.Bot):
    bot.add_cog(CConfiguration(bot))

def teardown(bot: discord.Bot):
    bot.remove_cog(__name__)

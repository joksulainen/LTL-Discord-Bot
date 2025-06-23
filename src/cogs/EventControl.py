import datetime

import discord
import discord.ext.commands as extCommands
from discord import ApplicationContext, Option, slash_command

from utils.json_wrappers import update_persistence
from LTLBot import LTLBot


class CogEventControl(extCommands.Cog, name=__name__):
    def __init__(self, bot: LTLBot):
        self.BOT = bot
        self.__cog_guild_ids__ = [bot.config.guild_id]
    
    
    # Application commands
    GROUP = discord.SlashCommandGroup("event")
    
    
    @GROUP.command(name="start", options=[
        Option(discord.VoiceChannel, name="channel", description="The voice channel to start the event in"),
        Option(discord.Role, name="exclude_role", description="Exclude users with the provided role", required=False)
    ])
    async def event_start(self, ctx: ApplicationContext, param_channel: discord.VoiceChannel, param_exclude_role: discord.Role | None = None):
        """Start a new event"""
        # guard clause to prevent an event from being started if one is already active
        if self.BOT.persistence.event_channel_id != 0:
            channel = self.BOT.get_channel(self.BOT.persistence.event_channel_id)
            
            await ctx.respond(
                (f"There is already an existing event happening in {channel.mention}" 
                    if channel is not None else "There is already an existing event"),
                ephemeral=True
            )
            return
        
        # acknowledge that the command has been received
        await ctx.defer(ephemeral=True)
        
        # init some lists
        participant_list: list[int] = list()
        channel_members: list[discord.Member] = param_channel.members
        
        # iterate over channel_members to remove users with the specified role
        if param_exclude_role is not None:
            for member in channel_members:
                if param_exclude_role in member.roles:
                    channel_members.remove(member)
        
        # iterate over channel_members to get their ids
        for member in channel_members:
            participant_list.append(member.id)
        
        # get the current timestamp
        timestamp = datetime.datetime.now(datetime.UTC).timestamp()
        
        # update persistence file and acknowledge completion of the operation
        update_persistence(
            self.BOT.persistence,
            event_channel_id=param_channel.id,
            participants=participant_list,
            starting_time=timestamp,
            ending_time=0.0
        )
        ## public facing message
        ### todo: write the actual thing
        ## command user facing message
        await ctx.respond(f"Started a new event in {param_channel.mention}", ephemeral=True)
    
    @GROUP.command(name="end")
    async def event_end(self, ctx: ApplicationContext):
        """End a running event"""
        # guard clause to prevent ending a non-existent event
        if self.BOT.persistence.event_channel_id == 0:
            await ctx.respond("There's no event running currently", ephemeral=True)
            return
        
        # acknowledge that the command has been received
        await ctx.defer(ephemeral=True)
        
        # get the channel object of where the event is running
        channel = self.BOT.get_channel(self.BOT.persistence.event_channel_id)
        
        # get the current timestamp
        timestamp = datetime.datetime.now(datetime.UTC).timestamp()
        
        # update persistence file and acknowledge completion of the operation
        update_persistence(
            self.BOT.persistence,
            event_channel_id=0,
            ending_time=timestamp
        )
        ## public facing message
        ### todo: write the actual thing
        ## command user facing message
        await ctx.respond((f"Event in {channel.mention} ended" if channel is not None else "Event ended"), ephemeral=True)


# Extension related functions
def setup(bot: LTLBot):
    bot.add_cog(CogEventControl(bot))

def teardown(bot: LTLBot):
    bot.remove_cog(__name__)

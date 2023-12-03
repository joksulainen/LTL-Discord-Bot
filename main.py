import os
import platform
import sys
import traceback

import discord
import discord.ext.commands as extCommands
from discord import ApplicationCommandInvokeError, ApplicationContext

import handlers.config
import handlers.persistence
import permission_decorators

# Print version and platform stuff
print("Python version:", platform.python_version())
print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
print("-------------------")


# Initialize intents and bot instance
intents = discord.Intents.none()
intents.guilds = True
intents.guild_reactions = True

BOT = discord.Bot(intents=intents)


# Event listeners
@BOT.event
async def on_ready():
    print(f"Logged in as {BOT.user}")

@BOT.event
async def on_application_command_error(ctx: ApplicationContext, error: ApplicationCommandInvokeError):
    match error:
        case extCommands.errors.MissingPermissions:
            await ctx.respond(f"You're missing the following permissions to use this command: {', '.join(error.missing_permissions)}", ephemeral=True)
        case extCommands.errors.NotOwner:
            await ctx.respond("You're not the owner of the bot", ephemeral=True)
        case extCommands.errors.CheckAnyFailure:
            await ctx.respond("You need to fulfill atleast one of these conditions to use this command:\n{}".format("".join(f'`{i}`\n' for i in error.errors)), ephemeral=True)
        case extCommands.errors.CommandOnCooldown:
            await ctx.respond(f"Command is on cooldown, try again in {error.retry_after:.2f}s", ephemeral=True)
        case permission_decorators.NotAdmin:
            await ctx.respond("You're not an admin of the bot", ephemeral=True)
        case permission_decorators.NotModerator:
            await ctx.respond("You're not a moderator of the bot", ephemeral=True)
        case _:
            error_string = "".join(traceback.format_exception(type(error), error, error.__traceback__))[:-1]
            print(error_string, file=sys.stderr)
            message_format = f"__**An error has occurred!**__\n```{error_string}```"
            await ctx.respond(message_format, ephemeral=True)


# Setup function
def setup():
    print("Loading config...")
    handlers.config.init_config("./config.json")
    print("Config loaded!")
    print("Loading persistent data...")
    result = handlers.persistence.init_persistence("./persistence.json")
    print("Loaded existing persistent data!" if result else "Generated new persistent file.")
    print("Loading cogs...")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            BOT.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename[:-3]}")
    print("All cogs loaded!")

# Run only if main script
if __name__ == "__main__":
    setup()
    print("Starting bot with token...")
    BOT.run(handlers.config.CONFIG.token)

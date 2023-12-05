import json
import os
import platform
import sys
import traceback

import discord
import discord.ext.commands as extCommands
from discord import ApplicationCommandInvokeError, ApplicationContext

import utils
from utils.json_wrappers import create_config, create_persistence, DEFAULT_CONFIG


CONFIG_PATH = "./config.json"
PERSISTENCE_PATH = "./persistence.json"


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
        case extCommands.errors.CheckAnyFailure():
            await ctx.respond("You need to fulfill atleast one of these conditions to use this command:\n{}".format("".join(f'`{i}`\n' for i in error.errors)), ephemeral=True)
        case extCommands.errors.MissingPermissions():
            await ctx.respond(f"You're missing the following permissions to use this command: {', '.join(error.missing_permissions)}", ephemeral=True)
        case extCommands.errors.NotOwner():
            await ctx.respond("You're not the owner of the bot", ephemeral=True)
        case extCommands.errors.CommandOnCooldown():
            await ctx.respond(f"Command is on cooldown, try again in {error.retry_after:.2f}s", ephemeral=True)
        case utils.permission_decorators.NotAdmin():
            await ctx.respond("You're not an admin of the bot", ephemeral=True)
        case utils.permission_decorators.NotModerator():
            await ctx.respond("You're not a moderator of the bot", ephemeral=True)
        case _:
            error_string = "".join(traceback.format_exception(type(error), error, error.__traceback__))[:-1]
            print(error_string, file=sys.stderr)
            await ctx.respond("Something went wrong!", ephemeral=True)


# Setup function
def setup():
    print("Loading config...")
    config = create_config(CONFIG_PATH)
    if config is None:
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        print(f"Created new config at '{CONFIG_PATH}'. Fill out the 'token' and 'guild_id' fields before starting the script again.")
        os.system("pause")
        sys.exit()
    BOT.config = config
    print("Config loaded!")
    print("Loading persistent data...")
    persistence, success = create_persistence(PERSISTENCE_PATH)
    BOT.persistence = persistence
    print("Loaded existing persistent data!" if success else "Generated new persistent file.")
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
    BOT.run(BOT.config.token)

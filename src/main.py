import json
import os
import platform
import sys
import traceback
from pathlib import Path

import discord
import discord.ext.commands as extCommands
from discord import ApplicationCommandInvokeError, ApplicationContext
from dotenv import load_dotenv

import utils
from LTLBot import LTLBot
from utils.json_wrappers import DEFAULT_CONFIG, create_config, create_persistence

CONFIG_PATH = (Path(__file__).parent / "config.json").resolve()
PERSISTENCE_PATH = (Path(__file__).parent / "persistence.json").resolve()
COG_PATH = (Path(__file__).parent / "cogs").resolve()


# Print version and platform stuff
print("Python version:", platform.python_version())
print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
print("-------------------")


# Load environment variables
load_dotenv()

# Initialize intents and bot instance
intents = discord.Intents(
    guilds = True,
    guild_reactions = True
)

BOT = LTLBot(intents=intents)


# Event listeners
@BOT.event
async def on_ready():
    print(f"Logged in as {BOT.user}")

@BOT.event
async def on_application_command_error(ctx: ApplicationContext, error: ApplicationCommandInvokeError):
    match error.original:
        case extCommands.errors.CheckAnyFailure:
            await ctx.respond("You need to fulfill atleast one of these conditions to use this command:\n{}"
                                .format(", ".join(f'`{i}`' for i in error.original.errors)), ephemeral=True)
        case extCommands.errors.CommandOnCooldown:
            await ctx.respond(f"Command is on cooldown, try again in {error.original.retry_after:.2f}s", ephemeral=True)
        case extCommands.errors.NotOwner:
            await ctx.respond("You're not the owner of the bot to use that command", ephemeral=True)
        case utils.permission_decorators.NotAdmin:
            await ctx.respond("You're not an admin of the bot to use that command", ephemeral=True)
        case _:
            error_string = "".join(traceback.format_exception(type(error), error, error.__traceback__))[:-1]
            print(error_string, file=sys.stderr)
            await ctx.respond("Something went wrong!", ephemeral=True)


# Global guild check
@BOT.check
def global_guild_check(ctx: ApplicationContext):
    return ctx.guild is not None


# Setup function
def setup():
    problems: list[str] = []
    if os.getenv("BOT_TOKEN") is None:
        problems.append("Environment variable 'BOT_TOKEN' is missing.")
    print("Loading config...")
    config = create_config(CONFIG_PATH)
    if config is None:
        with CONFIG_PATH.open("w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        raise SystemExit(f"Created new config at '{CONFIG_PATH}'. Fill out the 'guild_id' field before starting the script again.")
    BOT.config = config
    print("Config loaded!")
    print("Loading persistent data...")
    BOT.persistence, success = create_persistence(PERSISTENCE_PATH)
    print("Loaded existing persistent data!" if success else "Generated new persistent file.")
    print("Loading cogs...")
    for path in COG_PATH.iterdir():
        if path.name.endswith(".py") and not path.name.startswith("_"):
            BOT.load_extension(f"{path.parts[-2]}.{path.name[:-3]}")
            print(f"Loaded {path.name[:-3]}")
    print("All cogs loaded!")

# Run only if main script
if __name__ == "__main__":
    setup()
    print("Starting bot with token...")
    try:
        BOT.run(os.getenv("BOT_TOKEN"))
    except discord.errors.LoginFailure:
        print("Improper token passed to bot. Did you forget to change the token field in your config file?")

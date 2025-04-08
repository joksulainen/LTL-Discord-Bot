import discord

from utils.json_wrappers import Config, Persistence


class LTLBot(discord.Bot):
    config: Config
    persistence: Persistence
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

import discord
from discord.ui import View, Button


class ConfirmationView(View):
    """View for actions that require confirmation. `decision` is a bool or None if there is no response or the view timed out."""
    decision: bool | None = None
    
    def __init__(self, *, timeout: float = 30, **kwargs):
        super().__init__(timeout=timeout, disable_on_timeout=True, **kwargs)
        self.add_item(Button(label="Yes", style=discord.ButtonStyle.green))
        self.add_item(Button(label="No", style=discord.ButtonStyle.red))

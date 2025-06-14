import discord
from discord.ui import View, Button


class ConfirmationView(View):
    """View for actions that require confirmation. `decision` is a bool or None if there is no response or the view timed out."""
    decision: bool | None = None
    
    def __init__(self, *,
            timeout: float = 30,
            disable_on_timeout: bool = True,
            lbl_yes: str = "Yes",
            lbl_no: str = "No",
            **kwargs
        ):
        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout, **kwargs)
        self.add_item(Button(label=lbl_yes, style=discord.ButtonStyle.green))
        self.add_item(Button(label=lbl_no, style=discord.ButtonStyle.red))

import discord
from discord import ButtonStyle
from discord.ui import View, Button


class ConfirmationButton(Button):
    _action: bool
    
    def __init__(self, *, 
            action: bool,
            style: ButtonStyle = ButtonStyle.secondary,
            label: str,
            custom_id: str | None = None,
            emoji: discord.PartialEmoji | None = None
        ):
        self._action = action
        super().__init__(style=style, label=label, custom_id=custom_id, emoji=emoji)
    
    
    async def callback(self, interaction: discord.Interaction):
        if isinstance(self.view, ConfirmationView):
            self.view.decision = self._action
            self.view.disable_all_items()
            self.view.stop()

class ConfirmationView(View):
    """View for actions that require confirmation. `decision` is a bool or None if there is no response or the view timed out."""
    _authorId: int
    decision: bool | None = None
    
    def __init__(self, author: int, *,
            timeout: float = 30,
            lbl_yes: str = "Yes",
            lbl_no: str = "No",
            **kwargs
        ):
        self._authorId = author
        super().__init__(timeout=timeout, disable_on_timeout=True, **kwargs)
        self.add_item(ConfirmationButton(action=True, label=lbl_yes, style=ButtonStyle.green))
        self.add_item(ConfirmationButton(action=False, label=lbl_no, style=ButtonStyle.red))
    
    
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self._authorId
    
    async def on_check_failure(self, interaction: discord.Interaction):
        await interaction.respond("You're not the original author of this view!", ephemeral=True)

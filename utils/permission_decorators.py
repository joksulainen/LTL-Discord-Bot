from discord import ApplicationContext
from discord.ext.commands import CheckFailure, check


def is_admin():
    async def predicate(ctx: ApplicationContext) -> bool:
        if (not ctx.author.id in ctx.bot.config.admin_ids and
            not await ctx.bot.is_owner(ctx.author)):
            raise NotAdmin()
        return True
    return check(predicate)


class NotAdmin(CheckFailure):
    def __init__(self) -> None:
        super().__init__("Not admin")

import discord
import config


async def role_access(ctx) -> bool:
    """
    Checking access member to command
    :param ctx: message object
    :return: bool
    """
    for i in ctx.author.roles:
        if i.id == config.role_keeper or i.id == config.role_owner:
            return True
    else:
        return False


async def non_access(ctx) -> None:
    """
    Message with info about non access to command
    :param ctx: message object
    :return: None, but sends message
    """
    emb = discord.Embed(title=f'Нет доступа', color=0xFF0000)
    emb.set_footer(text='Комманда доступна только Хранителям Сокровищницы')
    await ctx.send(embed=emb)

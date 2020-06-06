import discord
import config


async def role_access(ctx) -> bool:
    """Checking access member to command"""
    for i in ctx.author.roles:
        if i.id in config.role_access:
            return True
    else:
        return False


async def non_access(ctx) -> None:
    """Message with info about non access to command"""
    emb = discord.Embed(title=f'Нет доступа', color=0xFF0000)
    emb.set_footer(text='Комманда доступна только Хранителям Сокровищницы')
    await ctx.send(embed=emb)

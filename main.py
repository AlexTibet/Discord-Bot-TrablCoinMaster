import discord
from discord.ext import commands

import sql_fun
import config
import access_verification as access


def on_find_member(member_id: str) -> print:
    """Checking user availability in the database. If there is no user, then add him"""
    if sql_fun.simple_find_member(member_id):
        print(member_id, 'member fined')
    else:
        print(member_id, 'Member not fined in DB.\nadd member in DB')
        for member in Bot.guilds[0].members:
            if member.id == member_id:
                sql_fun.add_user(member_id)
            else:
                print('Member not find in discord server')


if __name__ == '__main__':
    Bot = commands.Bot(command_prefix="th@")
    Bot.remove_command('help')


    @Bot.event
    async def on_ready():
        print(f"The bot has started!\nAnd it works on the server: {Bot.guilds[0].name}")
        await Bot.change_presence(status=discord.Status.online, activity=discord.Game('Считаем койны'))


    @Bot.event
    async def on_member_join(member):
        if not sql_fun.simple_find_member(member.id):
            sql_fun.add_user(member.id)


    @Bot.command()
    async def coins(ctx, nik_name=None):
        """info about member coins"""
        if nik_name is None:
            nik_name = ctx.author.id
        else:
            nik_name = nik_name.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
        on_find_member(nik_name)
        row = sql_fun.check_balance(nik_name)
        emb = discord.Embed(title=f'Cчёт: {row[0][1]} troublecoins', color=0xDAA520)
        emb.add_field(name=f'ID:{nik_name}', value=f'Счёт за всё время: {row[0][2]}')
        emb.set_thumbnail(url=config.img_url_mini_trouble)
        for i in ctx.guild.members:
            if int(nik_name) == int(i.id):
                nik_name = i
                break
        emb.set_author(name=f'Информация о баллансе:\n{nik_name}')
        await ctx.send(f"<@{ctx.author.id}>:\n", embed=emb)


    @Bot.command()
    # @Bot.has_role()
    async def coins_add(ctx, nik_name: str, add_value: str) -> None:
        """
        Add coins in account member and added coins in history (full_coins)

        Command access: only members with role "keeper"
        command: th@coins_add [nik_name "<@member_id>": str] [add_value: str]

        return message with embed info
        """
        nik_name = nik_name.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
        if await access.role_access(ctx):
            on_find_member(nik_name)
            tc = int(add_value)
            row = sql_fun.check_balance(nik_name)
            tca = row[0][1] + tc
            tcf = row[0][2] + tc
            sql_fun.update_balance_full(nik_name, tca, tcf)

            emb = discord.Embed(title=f'Счёт: {tca}',
                                color=0xDAA520
                                )
            emb.set_thumbnail(url=config.img_t_coin)

            emb.add_field(name='ID:{}'.format(nik_name), value=f'Счёт за всё время: {tcf}')

            emb.set_author(name=f'Пополнение баланса на {add_value} troublecoins!')

            emb.set_footer(text=f'{ctx.author} оформляет начисление {add_value} troublecoins на ваш счёт',
                           icon_url=config.img_t_coin
                           )
            await ctx.send("<@{0}>\n".format(nik_name), embed=emb)
        else:
            await access.non_access(ctx)


    @Bot.command()
    async def coins_remove(ctx, nik_name, re_value):
        """Снятие койнов со счёта"""
        nik_name = nik_name.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
        if await access.role_access(ctx):
            on_find_member(nik_name)
            tca = int(re_value)
            row = sql_fun.check_balance(nik_name)
            tca = row[0][1] - tca
            sql_fun.update_balance_tca(nik_name, tca)

            emb = discord.Embed(title=f'Счёт: {tca}', color=0xDAA520)
            emb.add_field(name=f'ID:{nik_name}', value=f'Счёт за всё время: {row[0][2]}')
            emb.set_author(name=f'Снятие со счёта {re_value} troublecoins!')
            emb.set_footer(text='{0} оформляет снятие {1} troublecoins с вашего счёта'.format(ctx.author, re_value))

            await ctx.send("<@{0}>\n".format(nik_name), embed=emb)
        else:
            await access.non_access(ctx)


    @Bot.command()
    async def coins_transfer(ctx, nik_name, transfer):
        """Перевод койнов со своего счёта на счёт другого игрока"""
        nik_name = nik_name.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
        if int(ctx.author.id) == int(nik_name):
            await ctx.send(f"<@!{ctx.author.id}> зачем делать переводы самому себе? :thinking:\n`Не надо так...`")
        else:
            on_find_member(ctx.author.id)
            on_find_member(nik_name)
            tra = int(transfer)
            row_au = sql_fun.check_balance(ctx.author.id)
            if row_au[0][1] < tra:
                emb = discord.Embed(title='Недостаточно средств', color=0x800000)
                emb.set_footer(text=f'На вашем счёте только {row_au[0][1]} troublecoins')
                await ctx.send(f"<@!{ctx.author.id}>\n", embed=emb)
            else:
                row_lu = sql_fun.check_balance(nik_name)
                trm = row_au[0][1] - tra
                tra += row_lu[0][1]
                sql_fun.update_balance_tca(ctx.author.id, trm)

                emb = discord.Embed(title=f'Счёт: {trm}', color=0xDAA520)
                emb.set_author(name=f'Снято со счёта {transfer} troublecoins')
                emb.set_footer(
                    text=f'{ctx.author} переводит {transfer} troublecoins на другой счёт',
                    icon_url=config.img_t_coin)
                await ctx.send(f"<@!{ctx.author.id}>", embed=emb)

                sql_fun.update_balance_tca(nik_name, tra)
                emb = discord.Embed(title=f'Счёт: {tra}', color=0xDAA520)
                emb.set_author(name=f'Пополнение счёта на {transfer} troublecoins!')
                emb.set_footer(text=f'{ctx.author} переводит {transfer} troublecoins на ваш счёт!',
                               icon_url=config.img_t_coin)
                await ctx.send(f"<@{nik_name}>\n", embed=emb)


    @Bot.command()
    async def fullcoins_add(ctx, nik_name, add_value):
        """Начисление койнов на счёт за всё время"""
        nik_name = nik_name.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
        if await access.role_access(ctx):
            on_find_member(nik_name)
            tc = int(add_value)
            row = sql_fun.check_balance(nik_name)
            tca = row[0][2] + tc
            sql_fun.update_balance_tcf(nik_name, tca)

            emb = discord.Embed(title=f'Счёт за всё время: {tca}', color=0xDAA520)
            emb.set_thumbnail(url=config.img_t_coin)
            emb.set_author(name=f'Пополнение счёта за всё время на {add_value}')
            emb.set_footer(
                text=f'{ctx.author} оформляет начисление {add_value} на ваш счёт за всё время',
                icon_url=config.img_t_coin
            )
            await ctx.send(f"<@{nik_name}>\n", embed=emb)
        else:
            await access.non_access(ctx)


    @Bot.command()
    async def fullcoins_remove(ctx, nik_name, re_value):
        """Снятие койнов со счёта за всё время"""
        nik_name = nik_name.replace('<', '').replace('!', '').replace('@', '').replace('>', '')
        if await access.role_access(ctx):
            on_find_member(nik_name)
            tc = int(re_value)
            row = sql_fun.check_balance(nik_name)
            tcr = row[0][2] - tc
            sql_fun.update_balance_tcf(nik_name, tcr)

            emb = discord.Embed(title=f'Счёт за всё время: {tcr}', color=0xDAA520)
            emb.set_thumbnail(url=config.img_t_coin)
            emb.set_author(name=f'Уменьшение счёта за всё время на {re_value}')
            emb.set_footer(
                text=f'{ctx.author} оформляет снятие {re_value} с вашего счёта за всё время',
                icon_url=config.img_t_coin
            )
            await ctx.send(f"<@{nik_name}>\n", embed=emb)
        else:
            await access.non_access(ctx)


    Bot.run(config.token)

import discord
from discord.ext import commands
import time
import json
import os
import asyncio
#импорты

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="+", intents=intents)
token = "ODY1MTcyNDkyMTA3Nzc2MDMw.YPAIrA.9DJdpiDqdlOqKriJV2wHDXKfXvQ"


#интенты токен и переменная бот


#On_ready и выдача роли
@bot.event
async def on_ready():
    print("Bot is online")

    channel = bot.get_channel(864458966343090186) #channel - переменная для отправки сообщений, когда бот онлай
    await channel.send(f"{bot.user.name}#{bot.user.discriminator} - online.\n <@!595998891934220339>") #Упоминает пользователя

    while True:
#
        with open("info.json", "r") as f: #привет жсон
            d = json.load(f)
#
        maxim = max(d, key=lambda x: d[x]) #это не максим. получаем пользователя с высшем показателем актива в войсе
#
        top_user = int(maxim) #переобразовываем в int
        allmembers = bot.get_all_members() #получаем всех пользоателей
        guild = bot.get_guild(864110648312201227) #guild для выдачи роли
        role = guild.get_role(864476325984731156) #получаем саму роль
#
        for member in allmembers:
            if member.id == top_user:
                await member.add_roles(role) #цикл для выдачи роли человеку с высшем показателем актива в войсе
#
        await asyncio.sleep(10*60) #пускай будет чекать лучшего через каждые 10мин


#лидерборд
@bot.command(name="lb")
async def leaderboard(ctx):

    with open('info.json', 'r') as f: #и снова жсон
        data = json.load(f)

    top_users = {
        k: v for k,
        v in sorted(
            data.items(),
            key=lambda item: item[1], #создаем табличку с топом пользователей
            reverse=True)}

    names = ''
    for postion, user in enumerate(top_users):
        names += f'{postion+1} - <@!{user}> - {top_users[user]} мин.\n' #делаем табличку - табличкой

    embed = discord.Embed(title="Топ войса 🎙", colour=discord.Colour.blurple()) #создаём эмбед
    embed.add_field(name="Люди", value=names, inline=False) #табличка жива
    await ctx.send(embed=embed) #отправка в чат


@bot.event
async def on_voice_state_update(member, before, after):
    seconds_online = {}
    author = member.id

    if before.channel is None and after.channel is not None:

        connect = time.time()

        seconds_online[author] = connect

    elif before.channel is not None and after.channel is None and author in seconds_online:

        disconect = time.time()

        e = round(disconect - seconds_online[author], 1)
        with open("info.json", "r") as f:
            q = json.load(f)

        q[f"{member.id}"] += e
        h = q[f"{member.id}"] / 60
        h = round(h, 2)
        q[f"{member.id}"] = h

        with open("info.json", "w") as f:
            json.dump(q, f)


@bot.event
async def on_member_join(member): #теперь, чтобы не ломать голову и записывать в жсон пользователя который подключится к каналу
    #я решил добавлять сразу в жсон как только кто нибудь подкулючится к серверу. да, это возможная ошибка но мне лень.

    with open("info.json", "r") as f: #дарова жсон
        data = json.load(f)

    data[f"{member.id}"] = 0 #значение выставим на 0(логично впринцепе)

    with open("info.json", "w") as f:
        json.dump(data, f) #ну и записываем

    welcome = bot.get_channel(864110648312201230) #канал для отправки приветствия
    guild = bot.get_guild(864110648312201227)  # получаем гуилд, нужен для эмбеда
    embed = discord.Embed(
        description=f"Добро пожаловать на сервер **{guild.name}**, {member.mention} <:love:865516529507893268>",
        colour=discord.Colour.green()) #сам эмбед и все его части

    embed.add_field(
        name="1",
        value="Правила сервера можно прочитать здесь > <#864407243746967562>", #фиелд первый
        inline=False
    )

    embed.add_field(
        name="2",
        value="Посмотреть доступные роли можно здесь > <#864406724211113984>", #второй
        inline=False
    )

    embed.add_field(
        name="3",
        value="Получить роли можно здесь > <#865157815865573396>", #третий
        inline=False
    )

    await welcome.send(embed=embed) #Отправляем


@bot.event
async def on_member_remove(member): #когда пользователь выходит убираем из жсона

    with open("info.json", "r") as f:
        data = json.load(f) #открываем жсон

    del data[f"{member.id}"] #делит

    with open("info.json", "w") as f:
        json.dump(data, f) #записываем новые данные


@bot.command()
async def say(ctx, *, str=None):
    if str is None:

        sayerror = discord.Embed(
            description='Не правильный синтаксис команды. *say [тескст]', #отправляем эмбед об ошибке в лс
            colour=discord.Colour.orange())

        await ctx.author.send(embed=sayerror) #я хз почему sayerror

    else:

        embed = discord.Embed(description=str, colour=discord.Colour.green()) #ембед с текстом

        await ctx.send(embed=embed) #отправляем эмбед
        await ctx.message.delete() #удаляем сообщение-комманду


@bot.command()
async def load(ctx, extension):
    if ctx.author.id == 595998891934220339:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Cogs is loaded!")
    else:
        await ctx.send("Ты бота разработал??? Мне кажется нет...")


@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == 595998891934220339:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send("Cogs is unloaded!")
    else:
        await ctx.send("Ты бота разработал??? Мне кажется нет...")


@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == 595998891934220339:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Cogs is reloaded!")
    else:
        await ctx.send("Ты бота разработал??? Мне кажется нет...")


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(token) #пекись моя сладость пекись


#"""
#вобще этот код мне было лень делать, поэтому вот както так. бот предназначен для одного сервера, но маожно его и  изменить.
#Надеюсь на искреннее понимание. Спасибо Jabka#6666[679691974663733363] что вразумил мне что [] лучше не юзать.
#И вообще сказал мне самому думать :animal_cat_kruto_ubeyte:
#А эмодзи дса тут не работают... ну ладно
#Created by Zef1rchik#2021[595998891934220339]
#All rights reserved
#"""
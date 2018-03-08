#!/usr/bin/python3
# -*- coding: utf8 -*-

import discord, asyncio
import configparser, random, sys, os
import logging, logging.handlers
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

client = discord.Client()
config = configparser.ConfigParser()
config.read('bot.cfg')

bot = commands.Bot(command_prefix='!', description="Wizzie's Bot")
# Config values
token = config.get('BOT_INFO', 'token')
owner = config.get('BOT_INFO', 'owner')
#print(allowed)

way = True

def logger():
    errformat = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt="[%d/%m/%Y %H:%M]")

    l = logging.getLogger("discord")
    l.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)

    if not os.path.exists('logs'):
        os.makedirs('logs')
    eh = logging.handlers.RotatingFileHandler(
        filename='logs/bot.log', encoding='utf-8', mode='a',
        maxBytes=10**7, backupCount=5)
    eh.setFormatter(errformat)

    l.addHandler(eh)

    return l

@bot.event
async def on_ready():
    print('Logged in as: ')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------------')

# Rate Limiting
# Is done by the @commands.cooldown(num per, seconds, BucketType)


# commands
@commands.cooldown(1, 60, BucketType.user)
@bot.command(description='Don\'t trigger me')
async def triggered():
    await bot.say('HOLY FUCK I\'M TRIGGERED')
    await bot.say('REEEEEEEEEEEEEEEEEEEEEEE')
    await bot.say()

@commands.cooldown(1, 60, BucketType.user)
@bot.command(description='But is he a bro?')
async def gamage():
    await bot.say('What a bro')

@commands.cooldown(1, 60, BucketType.user)
@bot.command(description='I will make the choice for you')
async def cs(*choices : str):
    await bot.say(random.choice(choices))

@commands.cooldown(1, 60, BucketType.user)
@bot.command()
async def clayton():
    num = random.randrange(start=1, stop=2)
    if num == 1:
        await bot.say(':^)')
    if num == 2:
        await bot.say('(^:')

@commands.cooldown(1, 60, BucketType.user)
@bot.command()
async def dilly():
    await bot.say('Dilly Dilly')

@commands.cooldown(1, 60, BucketType.user)
@bot.command()
async def crk():
    await bot.say('Praise be unto him! 🇫')
    # the reaction will have to be added later

@bot.event
async def on_message(message):
    sender = str(message.author)
    #print(sender)
    if message.content.startswith('thanks wizbot') or message.content.startswith('Thanks wizbot'):
        await bot.send_message(message.channel, 'No problem')
    elif message.content.startswith('!master') and sender == owner:
        await bot.send_message(message.channel, 'My master is {}'.format(owner))
    await bot.process_commands(message)

def startup():
    #oadCogs()
    l = logger() # Run the logger before anything else.
    bot.run(token)

startup()

#!/bin/python3
# -*- coding: utf8 -*-

import discord, logging, asyncio
import configparser, random
from discord.ext import commands

client = discord.Client()
config = configparser.ConfigParser()
config.read('bot.cfg')

bot = commands.Bot(command_prefix='!', description="Wizzie's Bot")
# Config values
token = config.get('BOT_INFO', 'token')
allowed = config.get('BOT_INFO', 'allowed')
#print(allowed)

def logger():
    errformat = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt="[%d/%m/%Y %H:%M]")

    l = logging.getLogger("discord")
    l.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)

    if not os.path.exists('settings/logs'):
        os.makedirs('settings/logs')
    eh = logging.handlers.RotatingFileHandler(
        filename='settings/logs/bot.log', encoding='utf-8', mode='a',
        maxBytes=10**7, backupCount=5)
    eh.setFormatter(errformat)

    l.addHandler(errhandler)

    return l

@bot.event
async def on_ready():
    print('Logged in as: ')
    print(client.user.name)
    print(client.user.id)
    print('------------------------')

# commands

@bot.command()
async def gamage(description='But is he a bro?'):
    await bot.say('What a bro')

@bot.command(description='Our lord and savior')
aysnc def crk(message):
    await bot.add_reaction(message, '🇫')
    await bot.say('Praise be to him!')

@bot.command(description='I will make the choice for you')
async def choose(*choices : str):
    await bot.say(random.choice(choices))

# @client.event
# async def on_message(message):
#     sender = str(message.author)
#     #print(sender)
#     if message.content.startswith('!test') and (allowed.find(sender) != -1):
#         #print("test message\n")
#         counter = 0
#         tmp = await client.send_message(message.channel, 'Calculating messages...')
#         async for log in client.logs_from(message.channel, limit=100):
#             if log.author == message.author:
#                 counter += 1
#         await client.edit_message(tmp, 'You have sent {} messages from the launch of the bot.'.format(counter))
#     elif message.content.startswith('!crk') or message.content.startswith('!Crk'):
#         await client.add_reaction(message, '🇫')
#         tmp = await client.send_message(message.channel, 'Praise be unto him!')
#         await client.add_reaction(tmp, '🇫')
#     elif message.content.startswith('🇫'):
#         await client.add_reaction(message, '🇫')
#     elif message.content.startswith('!sleep') and (allowed.find(sender) != -1):
#         await asyncio.sleep(5)
#         await client.send_message(message.channel, 'Done sleeping')

l = logger() # Run the logger before anything else.
client.run(token)

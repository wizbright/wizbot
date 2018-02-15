#!/bin/python3
# -*- coding: utf8 -*-

import discord, logging, asyncio
import configparser

client = discord.Client()
config = configparser.ConfigParser()
config.read('bot.cfg')

# Config values
token = config.get('BOT_INFO', 'token')
allowed = config.get('BOT_INFO', 'allowed')
#print(allowed)

def logger():
    l = logging.getLogger('discord')
    l.setLevel(logging.DEBUG)
    h = logging.FileHandler(filename="discord.log", encoding="utf8", mode="w")
    h.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    l.addHandler(h)

def permChecker(name):
    return true

@client.event
async def on_ready():
    print('Logged in as: ')
    print(client.user.name)
    print(client.user.id)
    print('------------------------')

@client.event
async def on_message(message):
    sender = str(message.author)
    #print(sender)
    if message.content.startswith('!test') and (allowed.find(sender) != -1):
        #print("test message\n")
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have sent {} messages from the launch of the bot.'.format(counter))
    elif message.content.startswith('!crk') or message.content.startswith('!Crk'):
        tmp = await client.send_message(message.channel, 'Praise be unto him!')
        await client.add_reaction(tmp, '🇫')
    elif message.content.startswith('!sleep') and (allowed.find(sender) != -1):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

logger() # Run the logger before anything else.
client.run(token)

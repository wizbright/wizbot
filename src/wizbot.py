#!/usr/bin/python3
# -*- coding: utf8 -*-

import discord, asyncio, re
import configparser, random, sys, os
import logging, logging.handlers
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord import Embed

client = discord.Client()
config = configparser.ConfigParser()
config.read('bot.cfg')

bot = commands.Bot(command_prefix='.', description="Wizzie's Bot")
# Config values
token = config.get('BOT_INFO', 'token')
owner = config.get('BOT_INFO', 'owner')
#print(allowed)

bot_logger = logger()

def dice_roll(num_sides: int, num_rolls: int = 1):
    rolls = []
    while range(num_rolls):
        rolls.append(random.randrange(1, num_sides+1))
    return rolls

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

@commands.cooldown(1, 69, BucketType.server)
@bot.command(description='eggplant..')
async def boner():
    await bot.say('🍆')

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

@commands.cooldown(5, 20, BucketType.user)
@bot.command(description='Roll some :game_die: boiiii')
async def dice(ctx,args):
    example = 'ex: `{0}dice d20` or `{0}dice 3d10+3`'.format(bot.command_prefix)
    roll_format = "[**{}**: {} =**{}**]"
    pattern = r'^(\d|10)d(4|6|10|12|20|100)([\+\-][1-9][0-9]?)?$'
    try:
        title = 'Dice Roll :game_die:'
        color = 'purple'
        description_elements = []
        for arg in args:
            if not re.match(pattern, arg):
                title = '**An Error Occurred**'
                description = '_Invalid formatting in:_ **{}**'.format(arg)
                color = 'red'
                raise ValueError('Incorrect formatting')
            else:
                pieces = re.match(pattern, arg).groups()
                rolls = dice_roll(int(pieces[1]), num_rolls = int(pieces[0]))
                rolls.append(int(pieces[2]))
                roll_amount = sum(rolls)
                roll_description = roll_format.format(arg, '+'.join(rolls), roll_amount)
                description_elements.append(roll_description)
        msg = Embed(
            title=title,
            description='\n'.join(description_elements),
            color=color
        )
        await bot.say(embed=msg)        
    except ValueError:
        bot_logger.info('Could not process dice roll: {}'.format(arg))
        msg = Embed(
            title=title,
            description='\n'.join[description, example],
            color=color
        )
        await bot.say(embed=msg)




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

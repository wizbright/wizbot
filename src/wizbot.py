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


def dice_roll(num_sides: int, num_rolls: int = 1):
    rolls = []
    for i in range(num_rolls):
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
async def ayy():
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
async def dice(*args):
    bot_logger = logger()
    example = "ex: `{0}dice d20` or `{0}dice 3d10+3`\nTry `{0}dice help` for more info".format(bot.command_prefix)
    roll_format = "[**{}**:{}**{}**]"
    pattern = r'^(\d|10)?d(4|6|10|12|20|100)([\+\-][1-9][0-9]?)?$'
    max_dice = 10
    max_args = 10
    try:
        title = 'Dice Roll :game_die:'
        color = discord.Color.purple()
        description_elements = []
        if len(args) < 1:
            title = '**An Error Occurred**'
            description = '_Not enough arguments_'
            color = discord.Color.red()
            raise ValueError('No args')
        if len(args) > max_args:
            title = '**An Error Occurred**'
            description = '_Too many arguments_: Max of {} rolls allowed'.format(max_args)
            color = discord.Color.red()
            raise ValueError('Too many args')
        if args[0] in ['help', '-h']:
            title = '**Dice Rolling Utility** :game_die:'
            description = [
                'Usage: `{0}dice [ROLL] [ROLL2] ...`',
                'Dice sides supported: 4, 6, 10, 12, 20, 100',
                'Max number of dice per roll: {1}',
                'Max number of rolls per command: {2}'
            ]
            description = "\n".join(description).format(bot.command_prefix, max_dice, max_args)
            color = discord.Color.blue()
            raise ValueError('Help wanted')
        for arg in args:
            if not re.match(pattern, arg):
                title = '**An Error Occurred**'
                description = '_Invalid formatting in:_ **{}**'.format(arg)
                color = discord.Color.red()
                raise ValueError('Incorrect formatting')
            else:
                num_rolls, die_size, modifier = re.match(pattern, arg).groups()
                if num_rolls is None:
                    num_rolls = 1
                rolls = dice_roll(int(die_size), num_rolls=int(num_rolls))
                if modifier is not None:
                    rolls.append(int(modifier))
                roll_amount = sum(rolls)
                if len(rolls) is 1:
                    roll_description = roll_format.format(arg, '', roll_amount)
                else:
                    roll_description = roll_format.format(arg, '+'.join([str(el) for el in rolls])+'=', roll_amount)
                description_elements.append(roll_description)
        msg = Embed(
            title=title,
            description='\n'.join([str(el) for el in description_elements]),
            color=color
        )
        await bot.say(embed=msg)        
    except ValueError as e:
        bot_logger.info('Could not process dice roll: {}'.format(e))
        msg = Embed(
            title=title,
            description='\n'.join([description, example]),
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

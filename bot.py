#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# TODO Files that are not updated that aren't in use
• music
• make on_message_edit catch banned words

# TODO Files that are being updated now

# TODO Files that are updated and in use (finished!)
• basic.py
• bot.py (duh)
• canvas.py # TODO doesnt send message when user doenst format correctly
• poll
• forwarding
• karma
• zalgo
• typeracer
• notifications
• verified
• admin

"""

import curtime
import settings

import os
import sys
import math
import time
import random
import asyncio
import aiohttp
import discord
import datetime
import numpy as np
from discord.ext import commands

# Cogs being used
extensions = ['accept', 'admin', 'basic', 'canvas', 'createpoll', 'forwarding', 'karma', 'typeracer', 'notifications', 'verified']

settings.set_server("main")  # make sure this is test or main


# Resets uptime settings
seconds = 0
minutes = 0
hours = 0
days = 0

ban_message = 0


# Defines Client
client = commands.Bot(description="synapsBot",
                      command_prefix='.',
                      owner_id="196355904503939073")


def get_json(file_path):
    with open(file_path, 'r') as fp:
        return json.load(fp)


async def timer():
    await client.wait_until_ready()
    global seconds
    seconds = 0
    global minutes
    minutes = 0
    global hours
    hours = 0
    global days
    days = 0
    while not client.is_closed:
        await asyncio.sleep(1)
        seconds += 1
        if seconds == 60:
            seconds = 0
            minutes += 1
            dirpath = os.getcwd()
            r = random.randint(1, 3)
            if r == 1:
                await client.change_presence(game=discord.Game(name="Live for {0}".format(curtime.uptime()),
                                                               url="https://twitch.tv/mehvix", type=1))
            if r == 2:
                await client.change_presence(game=discord.Game(name="Version {}".format(os.path.basename(dirpath)),
                                                               url="https://twitch.tv/mehvix", type=1))
            if r == 3:
                await client.change_presence(
                    game=discord.Game(name="Created by Mehvix#7172", url="https://twitch.tv/mehvix",
                                      type=1))
        elif minutes == 60:
            minutes = 0
            hours += 1

            fp = random.choice(os.listdir("media/avatars"))
            with open('media/avatars/{}'.format(fp), 'rb') as f:
                try:
                    await client.edit_profile(avatar=f.read())
                except discord.HTTPException:
                    pass  # Sometimes discord gets angry when the profile pic is changed a lot
        elif hours == 24:
            hours = 0
            days += 1


@client.event
async def on_connect():
    print("Connected!")


@client.event
async def on_ready():
    users = len(set(client.get_all_members()))
    channels = len([c for c in client.get_all_channels()])
    file_name = os.path.basename(sys.argv[0])  # Gets file name

    r = random.randint(2, 3)
    if r == 2:
        await client.change_presence(game=discord.Game(name="Version {}".format(file_name[10:-3]),
                                                       url="https://twitch.tv/mehvix", type=1))
    if r == 3:
        await client.change_presence(game=discord.Game(name="Created by Mehvix#7172", url="https://twitch.tv/mehvix",
                                                       type=1))
    server_list = list(client.guilds)
    dirpath = os.getcwd()

    print("=========================================================================")
    print("                                      ____        __  ____ _       __")
    print("   _______  ______  ____ _____  _____/ __ )____  / /_/ __ \ |     / /")
    print("  / ___/ / / / __ \/ __ `/ __ \/ ___/ __  / __ \/ __/ /_/ / | /| / /")
    print(" (__  ) /_/ / / / / /_/ / /_/ (__  ) /_/ / /_/ / /_/ _, _/| |/ |/ /")
    print("/____/\__, /_/ /_/\__,_/ .___/____/_____/\____/\__/_/ |_| |__/|__/")
    print("     /____/           /_/")
    print("• Bot Version:               {}".format(os.path.basename(dirpath)))
    print("• Discord Version:           {}".format(discord.__version__))
    print("• Python Version:            {}".format(sys.version.split()[0]))
    print("• Client Version:            {}".format(settings.get_version()))
    print("• Start Time:                {}".format(curtime.get_time()))
    print("• Client Name:               {}".format(client.user))
    print("• Client ID:                 {}".format(client.user.id))
    print("• Channels:                  {}".format(channels))
    print("• Users:                     {}".format(users))
    print("• Connected to " + str(len(client.guilds)) + " server(s):")
    for x in range(len(server_list)):
        print("     > " + server_list[x - 1].name)
    print("=========================================================================")


@client.event
async def on_resumed():
    print("{}: Resumed".format(curtime.get_time()))


# TODO Fix this
"""
@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send('This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.message.author.send('Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CheckFailure):
        await ctx.message.author.send('Sorry. You dont have permission to use this command.')
    elif isinstance(error, commands.MissingRequiredArgument):
        command = ctx.message.content.split()[1]
        await ctx.send("Missing an argument: " + command)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I don't know that command")
"""


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    client.loop.create_task(timer())
    client.run(settings.token)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO Items to rewrite/add logging to
• curtime
• settings


TODO New Commands
• Cool down
• Hearthstone cards (import hearthstone)
• Give XP for voice channel usage
• Remind me in x minutes
• GUI
• logging
• seeb server
• music bot
• twitter bot (leaks)
• slots
• poker
• minesweeper
• who has max level/karma
• nickname filter
• black jack
• .dog
• .copypasta (from r/copypasta)
• clever bot
• stats
• update help command(s)
• .aidan
• .aj
• https://i.redd.it/4iklecheyw601.jpg
• hearthstone stats
"""

import os
import sys
import math
import time
import random
import asyncio
import aiohttp
import curtime
import discord
import datetime
import settings
import numpy as np
from discord.ext import commands

'''
Make sure to change this to either 'test' or 'main'
'''
settings.set_server("test")


# Resets uptime settings
seconds = 0
minutes = 0
hours = 0
days = 0

ban_message = 0

# Cogs being used
extensions = []  #'admin', 'karma', 'basic', 'notifications', 'verified', 'createpoll', 'music', 'forwarding', 'typeracer', 'canvas'


# Defines Client
client = commands.Bot(description="synapsBot", command_prefix='.')

aiosession = aiohttp.ClientSession(loop=client.loop)


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
            file_name = os.path.basename(sys.argv[0])  # Gets file name
            r = random.randint(1, 3)
            if r == 1:
                await client.change_presence(game=discord.Game(name="Live for {0}".format(curtime.uptime()),
                                                               url="https://twitch.tv/mehvix", type=1))
            if r == 2:
                await client.change_presence(game=discord.Game(name="Version {}".format(file_name[10:-3]),
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

    print("============================================================")
    print("                                      ____        __")
    print("   _______  ______  ____  ____  _____/ __ )____  / /_")
    print("  / ___/ / / / __ \/ __ \/ __ \/ ___/ /_/ / __ \/ __/")
    print(" /__  / /_/ / / / / /_/ / /_/ /__  / /_/ / /_/ / /_")
    print("/____/\__  /_/ /_/\___,/ ____/____/_____/\____/\__/")
    print("     /____/           /_/\n")
    print("• Bot Version:               {}".format("Rewrite"))  # TODO make this based of file locatino (folder this is in
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
    print("============================================================")


@client.event
async def on_resumed():
    print("{}: Resumed".format(curtime.get_time()))


@client.event
async def on_message(message):
    times = 1

    # Message author variables
    user_id = message.author.id
    user_name = message.author

    # ".Accept" code
    if message.server:
        if message.channel.id == settings.accept_channel:
            role = discord.utils.get(message.server.roles, name=settings.member_role_name)
            if settings.member_role_id not in [role.id for role in message.author.roles]:
                if message.content.upper().startswith(".ACCEPT"):
                    await client.add_roles(user_name, role)
                    await asyncio.sleep(1)
                    await client.delete_message(message)
                    await client.send_message(discord.Object(id=settings.notification_channel),
                                              "<@{}> is now a Member :ok_hand:".format(user_id))
                    print("{0}: {1} joined the server (.accept)".format(curtime.get_time(), user_name))

                if message.content == '':
                    pass  # discord sends a embed message and this should pass it
                else:
                    await asyncio.sleep(.1)
                    try:
                        await client.delete_message(message)
                        print("{0}: DIDN'T type '.accept'".format(curtime.get_time(), user_name))
                    except discord.NotFound:  # If user types .accept it already deletes the message
                        pass
        else:
            pass
    else:
        return

    if message.content.upper().startswith("BAD BOT"):
        await client.send_message(message.channel, "Bad human")

    if message.content.upper().startswith("GIT "):
        word = message.content.split(" ")
        await client.send_message(message.channel, "`git: '{}' is not a git command. See 'git --help'.`".format(
            word[1]))

    if message.content.upper().startswith(".PING"):
        print("{0}: {1} activated 'PING".format(curtime.get_time(), user_name))
        msg = await client.send_message(message.channel, "Pinging...")

        start = time.time()
        async with aiosession.get("https://discordapp.com"):
            duration = time.time() - start
        duration = round(duration * 1000)
        await client.edit_message(msg, "I have a ping of `{}` ms (`1` try)".format(duration))
        ping = [duration]
        print(duration)

        while times < 5:
            start = time.time()
            async with aiosession.get("https://discordapp.com"):
                duration = time.time() - start
            duration = round(duration * 1000)
            print(duration)
            ping.append(duration)
            print(ping)
            mean = np.mean(ping)
            await client.edit_message(msg, "I have a ping of `{}` ms (`{}` / `4` tries)".format(mean, times))
            times += 1


@client.command()
async def load(extension_name: str):
    try:
        client.load_extension(extension_name)
        print("LOADED {}".format(extension_name))
    except (AttributeError, ImportError) as error:
        await print("```py\n{}: {}\n```".format(type(error).__name__, str(error)))
        return
    print("{} loaded.".format(extension_name))


@client.command()
async def unload(extension_name: str):
    client.unload_extension(extension_name)
    print("{} unloaded.".format(extension_name))


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    client.loop.create_task(timer())
    client.run(settings.token)
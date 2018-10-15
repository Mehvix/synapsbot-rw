#!/usr/bin/env python
# -*- coding: utf-8 -*-
# testing all branches are good.

""" ''''''''''''''''''''''''''''''''''''''''''
          TODOs are located on Trello:
    https://trello.com/b/CQBT9vag/synapsbot


          Code can be found on GitHub:
    https://github.com/Mehvix/synapsBotRW

'''''''''''''''''''''''''''''''''''''''''' """

import asyncio
import os
import random
import sys
from datetime import datetime

import discord
from discord.ext import commands

import karma
import curtime
import settings

# Cogs being used
extensions = ['accept', 'admin', 'basic', 'canvas', 'forwarding', 'karma', 'typeracer', 'notifications', 'games',
              'verified', 'reddit', 'qr', 'lobby_text', 'hearthstone_decode']

settings.set_server("main")  # make sure this is test or main

seconds = 0
ban_message = 0
users = 0

global before_invites, after_invites
before_invites = []
after_invites = []


def flair(num_of_users):  # todo: add more flairs
    flairs = ['Created by Mehvix#7172',
              'Running Version {}'.format(settings.get_version()),
              'Used by {} users!'.format(num_of_users),
              'Try .github for code',
              'Try .trello for upcoming stuff'
              ]
    return random.choice(flairs)


# Defines Client
client = commands.Bot(description="If you have any issues please contact @Mehvix#7172",
                      command_prefix='.',
                      owner_id="196355904503939073",
                      case_insensitive=True)

discord.ext.commands.HelpFormatter(show_hidden=False)


def get_json(file_path):
    with open(file_path, 'r') as fp:
        return json.load(fp)


async def timer():
    await client.wait_until_ready()
    global seconds
    while True:
        # "Who invited" code
        for guild in client.guilds:
            for invite in await guild.invites():
                x = [invite.url, invite.uses, invite.inviter.id]
                before_invites.append(x)

        await asyncio.sleep(59)  # sometimes this skips if it's on 60?

        # Presence
        await client.change_presence(
            activity=discord.Streaming(name=flair(users), url='https://twitch.tv/mehvix',
                                       twitch_name="Mehvix"))

        fp = random.choice(os.listdir("media/avatars"))
        with open('media/avatars/{}'.format(fp), 'rb') as f:
            try:
                await client.user.edit(avatar=f.read())
            except discord.HTTPException:
                pass  # Sometimes discord gets angry when the profile pic is changed a lot

        # Comic Code
        if str(str(str(datetime.now()).split(" ")[1]).split(".")[0])[:5] == "09:00":
            date = datetime.today().strftime('%Y/%m/%d')
            search = "https://www.gocomics.com/calvinandhobbes/{}".format(date)
            print(search)
            channel = client.get_channel(settings.notification_channel)
            await channel.send(search)
            await asyncio.sleep(2)


@client.event
async def on_member_join(member):
    for guild in client.guilds:
        for invite in await guild.invites():
            x = [invite.url, invite.uses, invite.inviter.id]
            after_invites.append(x)

        await asyncio.sleep(1)

        def diff(first, second):
            second = list(second)
            return [item for item in first if item not in second]

        invite_used = diff(after_invites, before_invites)
        invite_user = client.get_user(invite_used[0][2])

        if member.guild.name != "Bot Test":
            karma.user_add_karma(invite_user.id, 75)
            channel = client.get_channel(id=settings.notification_channel)
            await channel.send("<@{}> used an invited created by <@{}> which gave the invite creator `75` karma".
                               format(member.id, invite_user.id))


@client.event
async def on_connect():
    print("Connected!")


@client.event
async def on_ready():
    global users
    users = len(set(client.get_all_members()))
    channels = len([c for c in client.get_all_channels()])
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

    if len(client.guilds) > 1:
        print("ISSUE: It's not recommended to have more than one server being hosted at the same time.")

    await client.change_presence(
        activity=discord.Streaming(name=flair(users), url='https://twitch.tv/mehvix',
                                   twitch_name="Mehvix"))  # TODO add more presences


@client.event
async def on_resumed():
    print("{}: Resumed".format(curtime.get_time()))


@client.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command cannot be used in private messages.")

    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("Sorry. This command is disabled and cannot be used.")

    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry. You don't have permission to use this command.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a parameter. Do `.help [command name]` for more info")

    elif isinstance(error, commands.NotOwner):
        await ctx.send("Only the bot's owner can use this command")

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I need special permissions to use that command: \n{}".format(
            "\n ".join(commands.BotMissingPermissions.missing_perms)))

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You need special permissions to use that command: \n{}".format(
            "\n ".join(commands.MissingPermissions.missing_perms)))

    elif isinstance(error, commands.BadArgument):
        await ctx.send(error)

    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("You have too many arguments")

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            "That command is on a cooldown for `{}` more seconds. It can be used every `{}` seconds".format(
                commands.CommandOnCooldown.cooldown, str(commands.CommandOnCooldown.retry_after)[:5]))

    """
    elif isinstance(error, commands.BadArgument):
        command = ctx.message.content.split()[1]
        await ctx.send("Missing an argument: " + command)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I don't recognize that command")
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

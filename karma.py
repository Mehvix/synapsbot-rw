#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import os
import re#eeeeeeeeee

import discord
from discord.ext import commands

import settings


class Karma(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        super().__init__()
        self.client = client

    print("Loading Karma...")

    @commands.Cog.listener()
    async def on_ready(self):
        while self.client:
            for guild in self.client.guilds:
                for member in guild.members:
                    if \
                            member.voice \
                            and not member.voice.deaf \
                            and not member.voice.mute \
                            and not member.voice.self_deaf \
                            and not member.voice.self_mute \
                            and not member.voice.afk:
                        self.user_add_karma(member.id, 1)
            await asyncio.sleep(180)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):  # todo make raw
        upvote = "<{}>".format(settings.upvote_emoji)
        downvote = "<{}>".format(settings.downvote_emoji)

        if str(reaction.emoji) == upvote or downvote:
            if user != reaction.message.author:
                if str(reaction.emoji) == upvote:
                    self.user_add_karma(reaction.message.author.id, 5)
                if str(reaction.emoji) == downvote:
                    self.user_add_karma(reaction.message.author.id, -5)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        upvote = "<{}>".format(settings.upvote_emoji)
        downvote = "<{}>".format(settings.downvote_emoji)

        if str(reaction.emoji) == upvote or downvote:
            if user != reaction.message.author:
                if str(reaction.emoji) == upvote:
                    self.user_add_karma(reaction.message.author.id, -5)
                if str(reaction.emoji) == downvote:
                    self.user_add_karma(reaction.message.author.id, 5)

    @client.command(description="Finds out how much karma a user has", usage="[@user]", brief="Finds [@users] karma. If left blank it will find whoever sent the message's kamra")
    async def karma(self, ctx, *args):
        if args == ():
            user_req = ctx.message.author.id
        else:
            if not ctx.message.raw_mentions:
                await ctx.send("You need to `@` a user")
                return
            user_req = ctx.message.raw_mentions[0]

        try:
            await ctx.send("<@{0}> has `{1}` karma".format(user_req, get_karma(user_req)))
        except KeyError:
            await ctx.send("<@{0}> has `0` karma".format(user_req))

    @client.command(description="Finds out how high of a level a user has gotten", usage="[@user]", brief="Finds [@users] top level. If left blank it will find whoever sent the message's level")
    async def level(self, ctx, *args):
        if args == ():
            user_req = ctx.message.author.id
        else:
            if not ctx.message.raw_mentions:
                await ctx.send("You need to `@` a user")
                return
            user_req = ctx.message.raw_mentions[0]

        try:
            await ctx.send("<@{0}> is level `{1}`".format(user_req, get_level(user_req)))
        except KeyError:
            await ctx.send("<@{0}> is level `0`".format(user_req))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.webhook_id:
            return

        # Message author variables
        user_id = message.author.id
        user_name = message.author

        author_level = get_level(user_id)
        author_karma = get_karma(user_id)


        """
        # Because @xpoes#9244 spams the shit out of our pokemon channel
        if message.channel.id != settings.pokemon_channel:
            self.user_add_karma(user_id, 1)
        """

        # Adds upvote to images / uploads and URLS
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if re.match(regex, message.content) is not None or message.attachments:
            await message.add_reaction(settings.upvote_emoji)

        # Checks Karma / Level
        try:
            new_level = author_level + 1
        except TypeError:
            return  # webhook was sent

        if author_karma >= (500 * new_level) - 500:
            if user_id == self.client.user.id:
                return

            if new_level <= 27:
                level_role = discord.utils.get(message.guild.roles, name="Level {}".format(new_level))
                old_level_role = discord.utils.get(message.guild.roles, name="Level {}".format(int(new_level) - 1))

                set_level(user_id, new_level)

                """ This ~~shouldn't~~ happen
                if not level_role:
                    try:
                        pass  # I've anything past 100 shouldn't be counted
                        # role = await message.guild.create_role(name="Level {}".format(new_level))
                    except discord.HTTPException:
                        role = None
                        print("You have to many roles (>250)")
                    await message.author.add_roles(role)
                    await message.guild.owner.send("The bot manually created a role for <@{}> when they leveled up".format(user_id))
                """
                await message.author.add_roles(level_role)
                await message.author.remove_roles(old_level_role)
                """
                level1_role = discord.utils.get(message.guild.roles, name="Level 1")
                await message.author.remove_roles(level1_role)
                """
            await message.channel.send("Congrads, <@{}>! You're now level `{}`".format(user_id, new_level))

        self.user_add_karma(user_id, 1)

    def user_add_karma(self, user_id: int, karma: int):
        user_id = str(user_id)
        if os.path.isfile("users.json"):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id]['karma'] += karma
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
            except (TypeError, KeyError):
                try:
                    with open('users.json', 'r') as fp:
                        users = json.load(fp)
                    users[user_id] = {}
                    users[user_id]['karma'] = karma
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)
                except Exception as e:
                    exc = '{}: {}'.format(type(e).__name__, e)
                    print('Failed to load extension {}\n{}'.format(e, exc))
            x = self.client.get_user(int(user_id))
            set_name(user_id, x.name)
        else:
            users = {user_id: {}}
            users[user_id]['karma'] = karma
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)


def get_karma(user_id: int):
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        with open('users.json', 'r') as fp:
            users = json.load(fp)
        return users[user_id]['karma']

    else:
        return 0


def set_level(user_id: int, level: int):
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        with open('users.json', 'r') as fp:
            users = json.load(fp)
        users[user_id]["level"] = level
        with open('users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def set_name(user_id: str, name: str):
    user_id = str(user_id).replace('"', "'")
    if os.path.isfile('users.json'):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]["name"] = name
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except (TypeError, KeyError):
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = user_id
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)


def get_level(user_id: int):
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            return users[user_id]['level']
        except KeyError:
            set_level(int(user_id), 1)
            return 1


def setup(client):
    client.add_cog(Karma(client))

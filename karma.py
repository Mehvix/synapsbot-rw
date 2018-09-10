#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import discord
import curtime
import settings
from discord.ext import commands


class Karma:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Karma...")

    @client.event
    async def on_raw_reaction_add(self, reaction, user):  # TODO make this shit work
        emoji_used = str(reaction.emoji)
        formated_up = "<{}>".format(settings.upvote_emoji)
        formated_down = "<{}>".format(settings.downvote_emoji)

        print("{0}: {1} reacted with {2} to {3}'s message"
              .format(curtime.get_time(), user, emoji_used, reaction.message.author))

        if reaction.message.channel.id != settings.pokemon_channel:
            if emoji_used == formated_up:  # If emote is the upvote emote
                if reaction.message.author.id == user.id:
                    print("{0}: {1} upvoted there own link. NO CHANGE".format(curtime.get_time(), user))
                else:
                    try:
                        user_add_karma(reaction.message.author.id, 5)
                        print("{0}: ADDED 5 karma to {1} for a UPVOTE from {2}"
                              .format(curtime.get_time(), reaction.message.author, user))
                    except AttributeError:
                        print("{0}: User doesn't exist! (Probably a webhook)".format(curtime.get_time()))

            # If emote is the downvote emote
            if emoji_used == formated_down:
                if reaction.message.author.id == user.id:
                    print("{0}: {1} downvoted there post. NO CHANGE"
                          .format(curtime.get_time(), user))
                else:
                    try:
                        user_add_karma(reaction.message.author.id, -5)
                        print("{0}: REMOVED 5 karma from {1} for a DOWNVOTE from {2}"
                              .format(curtime.get_time(), reaction.message.author, user))
                    except AttributeError:
                        print("{0}: User doesn't exist! (Probably a webhook)".format(curtime.get_time()))
        else:
            print("{0}: DIDN'T change {1}'s karma because they're in the Pokemon Channel!"
                  .format(curtime.get_time(), user))

    @client.event
    async def on_raw_reaction_remove(self, reaction, user):
        emoji_used = str(reaction.emoji)
        formated_up = "<{}>".format(settings.upvote_emoji)
        formated_down = "<{}>".format(settings.downvote_emoji)

        if reaction.message.channel.id != settings.pokemon_channel:
            if emoji_used == formated_up:
                if reaction.message.author.id == user.id:
                    print("{0}: {1} REMOVED their upvote to their post. NO CHANGE".format(curtime.get_time(), user.id))
                else:
                    try:
                        user_add_karma(reaction.message.author.id, -5)
                        print("{0}: REMOVED 5 karma from {0} because {1} REMOVED there UPVOTE"
                              .format(curtime.get_time(), reaction.message.author, user))
                    except AttributeError:
                        print("{0}: User doesn't exist! (Probably a webhook)".format(curtime.get_time()))

            # If emote is the downvote emote
            if emoji_used == formated_down:
                if reaction.message.author.id == user.id:
                    print("{0}: {1} REMOVED their downvote to there own link. NO CHANGE".format(curtime.get_time(),
                                                                                                user))
                else:
                    try:
                        user_add_karma(reaction.message.author.id, 5)
                        print("{0}: RE-ADDED 5 karma to {1} for removal of downvote reaction from {2}"
                              .format(curtime.get_time(), reaction.message.author, user))
                    except AttributeError:
                        print("{0}: User doesn't exist! (Probably a webhook)".format(curtime.get_time()))
        else:
            print("{0}: DIDN'T change {1}'s karma because it was in the Pokemon Channel!"
                  .format(curtime.get_time(), user))

    @client.command()
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

    @client.command()
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

    @client.event
    async def on_message(self, message):
        # Message author variables
        user_id = message.author.id
        user_name = message.author

        try:
            author_level = get_level(user_id)
            author_karma = get_karma(user_id)
        except:
            author_level = None
            author_karma = None
            pass  # User just joined

        # Because @xpoes#9244 spams the shit out of our pokemon channel
        if message.channel.id != settings.pokemon_channel:
            user_add_karma(user_id, 1)

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

        if author_karma >= 100 * new_level:
            if user_id == self.client.user.id:
                return
            level_role = discord.utils.get(message.guild.roles, name="Level {}".format(new_level))
            old_level_role = discord.utils.get(message.guild.roles, name="Level {}".format(int(new_level) - 1))

            set_level(user_id, new_level)

            if not level_role:
                role = await message.guild.create_role(name="Level {}".format(new_level))
                await message.author.add_roles(role)
                await message.guild.owner.send("The bot manually created a role for <@{}> when they leveled up".format(user_id))

            level_role = discord.utils.get(message.guild.roles, name="Level {}".format(new_level))
            await message.author.add_roles(level_role)

            if message.channel.id != settings.canvas_channel or user_id != self.client.user.id:
                await message.channel.send("Congrats, <@{0}>! You're now level `{1}` :tada: ".format(user_id, new_level))

            await message.author.remove_roles(old_level_role)


def user_add_karma(user_id: int, karma: int):
    user_id = str(user_id)
    if os.path.isfile("users.json"):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]['karma'] += karma
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id] = {}
                users[user_id]['karma'] = karma
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

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


def get_level(user_id: int):
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            return users[user_id]['level']
        except KeyError:
            return 0


def setup(client):
    client.add_cog(Karma(client))

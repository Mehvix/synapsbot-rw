#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import curtime
import asyncio
import discord
import settings
from discord.ext import commands


class Basic:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Basic...")

    @client.command()
    async def about(self, ctx):
        info = await self.client.application_info()
        embed = discord.Embed(
            title="Info about {}:".format(info.name),
            description="• [Github](https://github.com/Mehvix/synapsBotRW)\n"
                        "• [Trello](https://trello.com/b/CQBT9vag/synapsbot)",
            color=settings.embed_color)
        embed.add_field(name="Creator:", value=info.owner, inline=True)
        embed.add_field(name="Python Version:", value=sys.version.split()[0], inline=True)
        embed.add_field(name="Discord.py Version:", value=discord.__version__, inline=True)
        embed.add_field(name="Client Version:", value=settings.get_version(), inline=True)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @client.command()
    async def trello(self, ctx):
        await ctx.send("Trello Link:\nhttps://trello.com/b/CQBT9vag/synapsbot")

    @client.command()
    async def issue(self, ctx):
        await ctx.send("Please report the issue here:\nhttps://github.com/Mehvix/synapsBotRW/issues")

    @client.command()
    async def ping(self, ctx):
        await ctx.send("I have a latency of `{}` ms".format(str(float(self.client.latency)*1000)[:2]))

    @client.event
    async def on_message(self, message):
        level_role = discord.utils.get(message.guild.roles, id=settings.level_role)
        roles_role = discord.utils.get(message.guild.roles, id=settings.roles_role)
        groups_role = discord.utils.get(message.guild.roles, id=settings.groups_role)
        games_role = discord.utils.get(message.guild.roles, id=settings.games_role)
        restriction_role = discord.utils.get(message.guild.roles, id=settings.restriction_role)
        level1_role = discord.utils.get(message.guild.roles, name="Level 1")
        if level_role and level_role not in message.author.roles:
            await message.author.add_roles(level_role,
                                           roles_role,
                                           groups_role,
                                           games_role,
                                           restriction_role,
                                           level1_role)
            print("Added Notation Roles")

        if message.author.id != self.client.user.id:
            channel = message.channel

            if "BAD BOT" in message.content.upper():
                await channel.send("Bad Human.")

            if "BOT BROKE" in message.content.upper():
                await channel.send("Please report the issue here:\nhttps://github.com/Mehvix/synapsBotRW/issues")

            if message.content.upper().startswith("GIT "):
                word = message.content.split(" ")
                await channel.send("`git: '{}' is not a git command. See 'git --help'.`".format(" ".join(word[1:])))

            if message.author.id != self.client.user.id:
                print("{}: {} sent '{}' in {}".format(curtime.get_time(), message.author.name, message.content,
                                                      message.channel.name))


def setup(client):
    client.add_cog(Basic(client))

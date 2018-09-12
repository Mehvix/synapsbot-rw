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
    async def ping(self, ctx):
        await ctx.send("I have a latency of `{}` ms".format(str(float(self.client.latency)*1000)[:2]))

    @client.event
    async def on_message(self, message):
        if message.author.id != self.client.user.id:
            channel = message.channel

            if message.content.upper().startswith("BAD BOT"):
                await channel.send("Bad Human.")

            if message.content.upper().startswith("GIT "):
                word = message.content.split(" ")
                await channel.send("`git: '{}' is not a git command. See 'git --help'.`".format(" ".join(word[1:])))

            if message.author.id != self.client.user.id:
                print("{}: {} sent '{}' in {}".format(curtime.get_time(), message.author.name, message.content,
                                                      message.channel.name))


def setup(client):
    client.add_cog(Basic(client))

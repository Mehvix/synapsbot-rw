#!/usr/bin/env python
# -*- coding: utf-8 -*-


import discord
import settings
from discord.ext import commands


class Cogname:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Cogname...")

    @commands.command()
    async def tester(self, ctx):
        print("TESTER ACTIVATED")

    @client.event
    async def on_message(self, message):
        if message.content == "live?":
            print("LIVE")


def setup(client):
    client.add_cog(Cogname(client))

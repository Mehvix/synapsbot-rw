#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class Cogname(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Cogname...")

    @commands.command(aliases=[""], usage="[usage]", description="Desc", brief="What it does")
    async def tester(self, ctx):
        print("TESTER ACTIVATED")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "live?":
            print("LIVE")


def setup(client):
    client.add_cog(Cogname(client))

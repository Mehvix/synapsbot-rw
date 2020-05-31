#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyqrcode

import discord
from discord.ext import commands


class QR(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading QR...")

    # TODO add png functionality
    @commands.command(aliases=["createqr", "qrcode"], usage="[data]", description="Creates an QR code", brief="Creates a QR code that links to [data]")
    async def qr(self, ctx, data):
        url = pyqrcode.create(data)
        with open('code.svg', 'wb') as fstream:
            url.svg(fstream, scale=5)

        await ctx.send(file=discord.File("code.svg"))


def setup(client):
    client.add_cog(QR(client))

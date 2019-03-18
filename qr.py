#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import pyqrcode

import discord
from discord.ext import commands


class QR(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading QR...")

    # TODO Fix this
    @commands.command(aliases=["createqr", "qrcode"], usage="[data]", description="Creates an QR code", brief="Creates a QR code that links to [data]")
    async def qr(self, ctx, data):
        url = pyqrcode.create(data)
        with open('code.png', 'wb') as fstream:
            url.png(fstream, scale=3)
        buffer = io.BytesIO()
        url.png(buffer)

        await ctx.send(file=discord.File("code.png"))


def setup(client):
    client.add_cog(QR(client))

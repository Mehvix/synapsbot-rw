#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
'forwarding.py' is port of a port from another bot:
Original:   https://github.com/jacobcheatley/dankbot
Import:     https://github.com/aikaterna/aikaterna-cogs/blob/master/away/away.py
"""


import discord
import settings
from discord.ext import commands


class Forwarding:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Forwarding...")

    @client.command()
    async def dmme(self, ctx):
        await ctx.message.author.send("DM!")

    async def on_message(self, message):
        my_id = 196355904503939073

        if not isinstance(message.channel, discord.abc.PrivateChannel) or message.channel.recipient.id == my_id:
            return

        # TODO Add more info (yoink from .whois command)
        embed = discord.Embed(color=settings.embed_color)
        if message.author == self.client.user:
            embed.title = 'Sent PM to {}#{} ({}).'.format(message.channel.recipient.name, message.channel.recipient.discriminator,
                                                          message.channel.recipient.id)
        else:
            embed.set_author(name=message.author,
                             icon_url=message.author.avatar_url or message.author.default_avatar_url)
            embed.title = '{} messaged me:'.format(message.channel.user.id)
        embed.description = "Clean Content:{}".format(message.clean_content)
        embed.timestamp = message.created_at

        user = await self.client.get_user_info(196355904503939073)
        await user.send(embed=embed)


def setup(client):
    client.add_cog(Forwarding(client))


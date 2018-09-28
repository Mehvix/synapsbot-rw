#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
'forwarding.py' is port of a port from another bot:
Original:   https://github.com/jacobcheatley/dankbot
Import:     https://github.com/aikaterna/aikaterna-cogs/blob/master/away/away.py
"""

import discord
from discord.ext import commands

import settings


class Forwarding:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Forwarding...")

    async def on_message(self, message):
        my_id = 196355904503939073

        if not isinstance(message.channel, discord.abc.PrivateChannel) or message.channel.recipient.id == my_id:
            return

        embed = discord.Embed(color=settings.embed_color)
        if message.author == self.client.user:
            embed.set_author(
                name='I sent a PM to {}#{} ({}).'.format(
                    message.channel.recipient.name, message.channel.recipient.discriminator, message.channel.recipient.id),
                icon_url=message.author.avatar_url or message.author.default_avatar_url)
        else:
            embed.set_author(name='{} ({}) messaged me:'.format(message.channel.recipient.name, message.channel.recipient.id),
                             icon_url=message.author.avatar_url or message.author.default_avatar_url)
        embed.description = "{}".format(message.clean_content)
        embed.timestamp = message.created_at

        user = await self.client.get_user_info(196355904503939073)
        await user.send(embed=embed)


def setup(client):
    client.add_cog(Forwarding(client))


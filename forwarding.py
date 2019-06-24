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


class Forwarding(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Forwarding...")

    async def on_message(self, message):
        # todo check that this still works
        if not isinstance(message.channel, discord.abc.PrivateChannel) or message.author.id == self.client.id:
            return

        embed = discord.Embed(color=settings.embed_color)
        if not message.author == self.client.user:
            '''
            embed.set_author(
                name='I sent a PM to {}#{} ({}).'.format(
                    message.channel.recipient.name, message.channel.recipient.discriminator, message.channel.recipient.id),
                icon_url=message.author.avatar_url or message.author.default_avatar_url)
            '''
            embed.set_author(name='{} ({}) messaged me:'.format(message.author.name, message.author.id),
                             icon_url=message.author.avatar_url or message.author.default_avatar_url)

            embed.description = "{}".format(message.clean_content)
            embed.timestamp = message.created_at

            user = await self.client.get_user_info(196355904503939073)
            await user.send(embed=embed)


def setup(client):
    client.add_cog(Forwarding(client))

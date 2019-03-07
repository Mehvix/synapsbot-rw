#!/usr/bin/env python
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

import curtime
import karma
import settings

ban_message = 0


class Notifications(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Notifications...")

    @client.event
    async def on_member_join(self, member):
        karma.user_add_karma(member.id, 1)

        member_created_at_date = str(member.created_at).split('.', 1)[0]
        avatar = member.avatar_url if member.avatar else member.default_avatar_url

        embed = discord.Embed(color=settings.embed_color)
        embed.set_author(name="{} joined the server! 🎉".format(member.name))
        embed.add_field(name="Username:", value="{}#{}".format(member.name, member.discriminator), inline=False)
        embed.add_field(name="Time Joined:", value=curtime.get_time(), inline=False)
        embed.add_field(name="Account Created at:", value=member_created_at_date, inline=False)
        embed.add_field(name="User Avatar URL", value=member.avatar_url)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="We now have {} members!".format(member.guild.member_count))
        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send(embed=embed)

        await member.send(
            "Thank you for joining the server! **After reading the rules** in <#{}> type `.accept` in the channel to "
            "gain access to other channels, or `.decline` if you don't agree with the terms".format(
                settings.accept_channel))


def setup(client):
    client.add_cog(Notifications(client))

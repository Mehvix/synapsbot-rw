#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import karma
import curtime
import discord
import settings
from discord.ext import commands

ban_message = 0


class Notifications:
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
        embed.set_author(name="{} joined the server!".format(member.name))
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

    @client.event
    async def on_member_ban(self, guild, member):
        global ban_message
        ban_message += 1
        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send("<@{}> was **banned** :hammer: \nYou can find out who banned them by checking the audit log".format(member.id))

    @client.event
    async def on_member_unban(self, guild,  member):
        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send(
            "<@{}> was **unbanned** :hammer: \nYou can find out who unbanned them by checking the audit log".format(
                member.id))

    @client.event
    async def on_member_remove(self, member):
        global ban_message
        if ban_message == 1:
            ban_message = 0
        else:
            channel = self.client.get_channel(id=settings.notification_channel)
            await channel.send("<@{}> was either kicked or left the server :frowning2:".format(member.id))
            ban_message = 0


def setup(client):
    client.add_cog(Notifications(client))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings

import discord
from discord.ext import commands


class lobbytext:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Lobbytext...")

    @client.event
    async def on_voice_state_update(self, member, before, after):
        role1 = discord.utils.get(member.guild.roles, id=settings.lobby_one_role_id)
        role2 = discord.utils.get(member.guild.roles, id=settings.lobby_two_role_id)

        await member.remove_roles(role1, role2)

        if after.channel is None:
            return  # user DC'd

        if after.channel.id == settings.lobby_one_vc_id:
            await member.add_roles(role1)
            return

        if after.channel.id == settings.lobby_two_vc_id:
            await member.add_roles(role2)
            return


def setup(client):
    client.add_cog(lobbytext(client))

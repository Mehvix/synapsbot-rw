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

        lobby1text = discord.utils.get(member.guild.text_channels, id=settings.lobby_one_text_id)
        lobby2text = discord.utils.get(member.guild.text_channels, id=settings.lobby_two_text_id)

        lobby1voice = discord.utils.get(member.guild.voice_channels, id=settings.lobby_one_vc_id)
        lobby2voice = discord.utils.get(member.guild.voice_channels, id=settings.lobby_two_vc_id)

        hidden_group = discord.utils.get(member.guild.categories, id=settings.hidden_cat_id)
        main_group = discord.utils.get(member.guild.categories, id=settings.main_cat_id)
        await member.remove_roles(role1, role2)

        if after.channel is None:
            print("user dc'd")

        if after.channel == lobby1voice:
            print("user moved into lobby 1")
            await lobby1text.edit(category=main_group, position=2)
            await member.add_roles(role1)

        if after.channel == lobby2voice:
            print("user moved into lobby 2")
            await lobby1text.edit(category=main_group, position=2)
            await member.add_roles(role2)

        if lobby1voice.members and lobby2voice.members:
            print("pll are in lobby 1 and 2")
            await lobby1text.edit(category=main_group, position=1)
            await lobby2text.edit(category=main_group, position=2)

            return

        if lobby1voice.members:
            print("pll are in lobby 1, {}".format(len(lobby1voice.members)))
            await lobby2text.edit(category=hidden_group, position=2)
            return

        if lobby2voice.members:
            print("pll are in lobby 2, {}".format(len(lobby2voice.members)))
            await lobby1text.edit(category=hidden_group, position=1)
            return

        await lobby1text.edit(category=hidden_group, position=1)
        await lobby2text.edit(category=hidden_group, position=2)
        print(after.channel.members)


def setup(client):
    client.add_cog(lobbytext(client))

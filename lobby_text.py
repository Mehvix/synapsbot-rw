#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings

import discord
from discord.ext import commands


class lobbytext:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Lobby Text...")

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

        if after.channel is None:
            pass  # user DC'd

        if after.channel == lobby2voice:
            await member.remove_roles(role1)
            await member.add_roles(role2)

        if after.channel == lobby1voice:
            await member.remove_roles(role2)
            await member.add_roles(role1)

        if lobby1voice.members and lobby2voice.members:
            await lobby1text.edit(category=main_group, position=6)
            await lobby2text.edit(category=main_group, position=7)
            return

        if lobby2voice.members:
            await lobby2text.edit(category=main_group, position=7)
            await lobby1text.edit(category=hidden_group, position=1)
            return

        if lobby1voice.members:
            await lobby1text.edit(category=main_group, position=6)
            await lobby2text.edit(category=hidden_group, position=2)
            return

        await lobby1text.edit(category=hidden_group, position=1)
        await lobby2text.edit(category=hidden_group, position=2)


def setup(client):
    client.add_cog(lobbytext(client))

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio
import discord
import settings
from discord.ext import commands


class Accept:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Accept...")

    @commands.command(hidden=True)
    async def decline(self, ctx):
        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send("<@{}> typed `.decline` and was kicked LUL".format(ctx.message.author.id))
        invite = await ctx.channel.create_invite(
            temporary=True, unique=True, reason="{} ({}) typed .decline instead of .accept".format(
                ctx.message.author.name, ctx.message.author.id))
        await ctx.message.author.send("Here's an invite if you change your mind!\n{}".format(invite.url))
        await ctx.message.author.kick()

    @commands.command(hidden=True)
    async def accept(self, ctx):
        member_role = discord.utils.get(ctx.guild.roles, name=settings.member_role_name)
        if member_role is None:
            try:
                member_role = await ctx.guild.create_role(name=member_role_name, color=discord.Color(0x939393))
            except discord.Forbidden:
                await ctx.guild.owner.send(
                    "I tried to create a roll called `{}` in `{}` but don't have the permission to!".format(member_role_name, ctx.guild.name))
        if member_role in ctx.author.roles:
            return  # User already has the role
        else:
            await ctx.message.author.add_roles(member_role, reason="User typed `.accept` in {}".format(ctx.channel))
            channel = self.client.get_channel(id=settings.notification_channel)
            await channel.send("<@{}> typed `.accept` :ok_hand:".format(ctx.author.id))

    @client.event
    async def on_message(self, message):
        if message.channel.id == settings.accept_channel and message.author.id != self.client.user.id:
            level_role = discord.utils.get(message.guild.roles, id=settings.level_role)
            if level_role and level_role not in member.roles:
                roles_role = discord.utils.get(message.guild.roles, id=settings.roles_role)
                groups_role = discord.utils.get(message.guild.roles, id=settings.groups_role)
                games_role = discord.utils.get(message.guild.roles, id=settings.games_role)
                restriction_role = discord.utils.get(message.guild.roles, id=settings.restriction_role)
                level1_role = discord.utils.get(message.guild.roles, name="Level 1")

                await member.add_roles(level_role, roles_role, groups_role, games_role, restriction_role, level1_role,
                                       reason="Added notation roles")
            await asyncio.sleep(1)

            try:
                await message.delete()
            except discord.NotFound:
                pass  # message already gone (deleted)


def setup(client):
    client.add_cog(Accept(client))

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

    @commands.command()
    async def decline(self, ctx):
        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send("<@{}> typed `.decline` and was kicked LUL".format(ctx.message.author.id))
        invite = await ctx.channel.create_invite(
            temporary=True, unique=True, reason="{} ({}) typed .decline instead of .accept".format(
                ctx.message.author.name, ctx.message.author.id))
        await ctx.message.author.send("Here's an invite if you change your mind!\n{}".format(invite.url))
        # TODO make this send user a DM with an invite back
        await ctx.message.author.kick()

    @commands.command()
    async def accept(self, ctx):
        member_role_name = settings.member_role_name
        member_role = discord.utils.get(ctx.guild.roles, name=member_role_name)
        if member_role is None:
            try:
                member_role = await ctx.guild.create_role(name=member_role_name, color=discord.Color(0x939393))
            except discord.Forbidden:
                await ctx.guild.owner.send(
                    "I tried to create a roll called `{}` in `{}` but don't have the permission to!".format(member_role_name, ctx.guild.name))
        if member_role in ctx.author.roles:
            return  # User already has the role
        else:
            try:
                await ctx.message.author.add_roles(member_role, reason="User typed `.accept` in {}".format(ctx.channel))
                channel = self.client.get_channel(id=settings.notification_channel)
                await channel.send("<@{}> typed `.accept` :ok_hand:".format(ctx.author.id))

            except discord.Forbidden:
                await ctx.guild.owner.send(
                    "I tried to add role `{}` to `{}` in `{}` but don't have the permission to!".format(member_role_name, ctx.author.name, ctx.guild.name))

    @client.event
    async def on_message(self, message):
        if message.channel.id == settings.accept_channel and message.author.id != self.client.user.id:
            await asyncio.sleep(1)
            try:
                await message.delete()
            except discord.Permissions:
                await ctx.guild.owner.send(
                    "I tried to clear a message in {}, but I don't have the permission to!".format(message.channel.name))
            except discord.NotFound:
                pass  # message already gone



def setup(client):
    client.add_cog(Accept(client))

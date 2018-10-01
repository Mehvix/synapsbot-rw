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

        global before_invites, after_invites
        before_invites = []
        after_invites = []

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
        if member_role is None:  # If server doesn't have member role
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
    async def on_ready(self):
        for guild in self.client.guilds:
            for invite in await guild.invites():
                x = [invite.url, invite.uses, invite.inviter.id]
                before_invites.append(x)
            print(before_invites)

    @client.event
    async def on_member_join(self, member):
        for guild in self.client.guilds:
            for invite in await guild.invites():
                x = [invite.url, invite.uses, invite.inviter.id]
                after_invites.append(x)
            print("--")
            print(before_invites)
            print(after_invites)
            print("--")

            await asyncio.sleep(1)

            def diff(first, second):
                second = list(second)
                return [item for item in first if item not in second]

            invite_used = diff(after_invites, before_invites)
            invite_user = self.client.get_user(invite_used[0][2])
            print("{} was invited by {}".format(member.name, invite_user.name))

    @client.event
    async def on_message(self, message):
        if message.channel.id == settings.accept_channel and message.author.id != self.client.user.id:
            level_role = discord.utils.get(message.guild.roles, id=settings.level_role)
            if level_role and level_role not in message.author.roles:
                roles_role = discord.utils.get(message.guild.roles, id=settings.roles_role)
                groups_role = discord.utils.get(message.guild.roles, id=settings.groups_role)
                games_role = discord.utils.get(message.guild.roles, id=settings.games_role)
                restriction_role = discord.utils.get(message.guild.roles, id=settings.restriction_role)
                level1_role = discord.utils.get(message.guild.roles, name="Level 1")

                await message.author.add_roles(level_role, roles_role, groups_role, games_role, restriction_role, level1_role,
                                       reason="Added notation roles")
            await asyncio.sleep(1)
            try:
                await message.delete()
            except discord.NotFound:
                pass  # message already gone (deleted)


def setup(client):
    client.add_cog(Accept(client))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import karma
import settings


class Games(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client
        self.letters = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇾', '🇽', '🇿']

    print("Loading Games...")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if list(set(after.roles) - set(before.roles)):
            new_role = list(set(after.roles) - set(before.roles))
            status = " added"

        if list(set(before.roles) - set(after.roles)):
            new_role = list(set(before.roles) - set(after.roles))
            status = " removed"

        try:
            for role in new_role:
                print(before.name + " had " + role.name + status)
        except UnboundLocalError:
            pass  # If user is updated but a role isn't add/removed

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            if int(payload.message_id) == settings.games_message_id:
                style = settings.game_roles
            else:
                style = settings.group_roles

            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name

            x = [x for x in self.letters if x == reaction]  # Checks if reaction is a letter
            location = self.letters.index("".join(x))  # Checks the location of the letter
            role = discord.utils.get(guild.roles, id=int(style[location]))  # Gets role
            await user.add_roles(role)

            # I was really tempted to do this: await user.add_roles(discord.utils.get(guild.roles,
            # id=int(style[self.letters.index("".join([x for x in self.letters if x == reaction]))])))


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            if int(payload.message_id) == settings.games_message_id:
                style = settings.game_roles
            else:
                style = settings.group_roles
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name

            x = [x for x in self.letters if x == reaction]  # Checks if reaction is a letter
            location = self.letters.index("".join(x))  # Checks the location of the letter
            role = discord.utils.get(guild.roles, id=int(style[location]))  # Gets role
            await user.remove_roles(role)

    @client.command(hidden=True)
    @commands.has_role(settings.admin_role_name)
    async def games(self, ctx):
        text = []
        for x in settings.game_roles:
            text.append(self.letters[settings.game_roles.index(x)] + " " + discord.utils.get(ctx.guild.roles, id=int(settings.game_roles[settings.game_roles.index(x)])).name)

        embed = discord.Embed(color=settings.embed_color, title="Games:",
                              description="\n".join(text))

        try:
            msg = await ctx.channel.get_message(settings.games_message_id)
            await msg.edit(embed=embed)
        except discord.NotFound:
            msg = await ctx.send(embed=embed)

        for reaction in self.letters[:len(str(msg.embeds[0].description).split("\n"))]:
            await msg.add_reaction(reaction)

        await ctx.message.delete()

    @client.command(hidden=True)
    @commands.has_role(settings.admin_role_name)
    async def groups(self, ctx):
        text = []
        for x in settings.group_roles:
            text.append(self.letters[settings.group_roles.index(x)] + " " + discord.utils.get(ctx.guild.roles, id=int(settings.group_roles[settings.group_roles.index(x)])).name)

        embed = discord.Embed(color=settings.embed_color, title="Groups:",
                              description="\n".join(text))

        try:
            msg = await ctx.channel.get_message(settings.groups_message_id)
            await msg.edit(embed=embed)
        except discord.NotFound:
            msg = await ctx.send(embed=embed)

        for reaction in self.letters[:len(str(msg.embeds[0].description).split("\n"))]:
            await msg.add_reaction(reaction)

        await ctx.message.delete()


def setup(client):
    client.add_cog(Games(client))

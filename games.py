#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import settings


class Games:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Games...")

    @client.event  # TODO make cam blacklisted
    async def on_raw_reaction_add(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name
            if str(reaction) == '🇦':
                role = discord.utils.get(guild.roles, id=settings.league_role)
                await user.add_roles(role)
            if str(reaction) == '🇧':
                role = discord.utils.get(guild.roles, id=settings.hs_role)
                await user.add_roles(role)
            if str(reaction) == '🇨':
                role = discord.utils.get(guild.roles, id=settings.fortnite_role)
                await user.add_roles(role)
            if str(reaction) == '🇩':
                role = discord.utils.get(guild.roles, id=settings.pubg_role)
                await user.add_roles(role)
            if str(reaction) == '🇪':
                role = discord.utils.get(guild.roles, id=settings.tf2_role)
                await user.add_roles(role)
            if str(reaction) == '🇫':
                role = discord.utils.get(guild.roles, id=settings.gta_role)
                await user.add_roles(role)
            if str(reaction) == '🇬':
                role = discord.utils.get(guild.roles, id=settings.chiv_role)
                await user.add_roles(role)
            if str(reaction) == '🇭':
                role = discord.utils.get(guild.roles, id=settings.cs_role)
                await user.add_roles(role)
            if str(reaction) == '🇮':
                role = discord.utils.get(guild.roles, id=settings.aoe_role)
                await user.add_roles(role)
            if str(reaction) == '🇯':
                role = discord.utils.get(guild.roles, id=settings.civ_role)
                await user.add_roles(role)
            if str(reaction) == '🇰':
                role = discord.utils.get(guild.roles, id=settings.rainbow_role)
                await user.add_roles(role)
            if str(reaction) == '🇱':
                role = discord.utils.get(guild.roles, id=settings.brawl_role)
                await user.add_roles(role)
            if str(reaction) == '🇲':
                role = discord.utils.get(guild.roles, id=settings.ratz_role)
                await user.add_roles(role)

    @client.event
    async def on_raw_reaction_remove(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name
            if str(reaction) == '🇦':
                role = discord.utils.get(guild.roles, id=settings.league_role)
                await user.remove_roles(role)
            if str(reaction) == '🇧':
                role = discord.utils.get(guild.roles, id=settings.hs_role)
                await user.remove_roles(role)
            if str(reaction) == '🇨':
                role = discord.utils.get(guild.roles, id=settings.fortnite_role)
                await user.remove_roles(role)
            if str(reaction) == '🇩':
                role = discord.utils.get(guild.roles, id=settings.pubg_role)
                await user.remove_roles(role)
            if str(reaction) == '🇪':
                role = discord.utils.get(guild.roles, id=settings.tf2_role)
                await user.remove_roles(role)
            if str(reaction) == '🇫':
                role = discord.utils.get(guild.roles, id=settings.gta_role)
                await user.remove_roles(role)
            if str(reaction) == '🇬':
                role = discord.utils.get(guild.roles, id=settings.chiv_role)
                await user.remove_roles(role)
            if str(reaction) == '🇭':
                role = discord.utils.get(guild.roles, id=settings.cs_role)
                await user.remove_roles(role)
            if str(reaction) == '🇮':
                role = discord.utils.get(guild.roles, id=settings.aoe_role)
                await user.remove_roles(role)
            if str(reaction) == '🇯':
                role = discord.utils.get(guild.roles, id=settings.civ_role)
                await user.remove_roles(role)
            if str(reaction) == '🇰':
                role = discord.utils.get(guild.roles, id=settings.rainbow_role)
                await user.remove_roles(role)
            if str(reaction) == '🇱':
                role = discord.utils.get(guild.roles, id=settings.brawl_role)
                await user.remove_roles(role)
            if str(reaction) == '🇲':
                role = discord.utils.get(guild.roles, id=settings.ratz_role)
                await user.remove_roles(role)

    @client.command()
    @commands.has_role(settings.admin_role_name)
    async def games(self, ctx):
        letters = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲']  # '🇳', '🇴'

        embed = discord.Embed(color=settings.embed_color, title="Games:",
                              description='🇦 League\n'
                                          '🇧 Hearthstone\n'
                                          '🇨 Fortnite\n'
                                          '🇩 PUBG\n'
                                          '🇪 TF2\n'
                                          '🇫 GTA V\n'
                                          '🇬 Chivalry\n'
                                          '🇭 CS:GO\n'
                                          '🇮 Age of Empires 2\n'
                                          '🇯 Civilization V\n'
                                          '🇰 Rainbow 6 Siege\n'
                                          '🇱 Brawlhalla\n'
                                          '🇲 Ratz Instagib\n')

        try:
            msg = await ctx.channel.get_message(490768003080650755)
            await msg.edit(embed=embed)
        except discord.NotFound:
            msg = await ctx.send(embed=embed)

        for reaction in letters[:len(letters)]:
            await msg.add_reaction(reaction)

        await ctx.message.delete()


def setup(client):
    client.add_cog(Games(client))

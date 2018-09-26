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

    @client.event
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

    @client.event
    async def on_ready(self):
        for guild in self.client.guilds:
            global league, hs, fortnite, pubg, tf2, gta, chiv, cs, aoe, civ, rainbow, brawl, ratz

            league = discord.utils.get(guild.roles, id=settings.league_role)
            hs = discord.utils.get(guild.roles, id=settings.hs_role)
            fortnite = discord.utils.get(guild.roles, id=settings.fortnite_role)
            pubg = discord.utils.get(guild.roles, id=settings.pubg_role)
            tf2 = discord.utils.get(guild.roles, id=settings.tf2_role)
            gta = discord.utils.get(guild.roles, id=settings.gta_role)
            chiv = discord.utils.get(guild.roles, id=settings.chiv_role)
            cs = discord.utils.get(guild.roles, id=settings.cs_role)
            aoe = discord.utils.get(guild.roles, id=settings.aoe_role)
            civ = discord.utils.get(guild.roles, id=settings.civ_role)
            rainbow = discord.utils.get(guild.roles, id=settings.rainbow_role)
            brawl = discord.utils.get(guild.roles, id=settings.brawl_role)
            ratz = discord.utils.get(guild.roles, id=settings.ratz_role)

    @client.event  # TODO make cam blacklisted
    async def on_raw_reaction_add(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name

            if str(reaction) == '🇦':
                await user.add_roles(league)  # TODO blacklist cam from this
            if str(reaction) == '🇧':
                await user.add_roles(hs)
            if str(reaction) == '🇨':
                await user.add_roles(fortnite)
            if str(reaction) == '🇩':
                await user.add_roles(pubg)
            if str(reaction) == '🇪':
                await user.add_roles(tf2)
            if str(reaction) == '🇫':
                await user.add_roles(gta)
            if str(reaction) == '🇬':
                await user.add_roles(chiv)
            if str(reaction) == '🇭':
                await user.add_roles(cs)
            if str(reaction) == '🇮':
                await user.add_roles(aoe)
            if str(reaction) == '🇯':
                await user.add_roles(civ)
            if str(reaction) == '🇰':
                await user.add_roles(rainbow)
            if str(reaction) == '🇱':
                await user.add_roles(brawl)
            if str(reaction) == '🇲':
                await user.add_roles(ratz)

    @client.event
    async def on_raw_reaction_remove(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name
            if str(reaction) == '🇦':
                await user.remove_roles(league)
            if str(reaction) == '🇧':
                await user.remove_roles(hs)
            if str(reaction) == '🇨':
                await user.remove_roles(fortnite)
            if str(reaction) == '🇩':
                await user.remove_roles(pubg)
            if str(reaction) == '🇪':
                await user.remove_roles(tf2)
            if str(reaction) == '🇫':
                await user.remove_roles(gta)
            if str(reaction) == '🇬':
                await user.remove_roles(chiv)
            if str(reaction) == '🇭':
                await user.remove_roles(cs)
            if str(reaction) == '🇮':
                await user.remove_roles(aoe)
            if str(reaction) == '🇯':
                await user.remove_roles(civ)
            if str(reaction) == '🇰':
                await user.remove_roles(rainbow)
            if str(reaction) == '🇱':
                await user.remove_roles(brawl)
            if str(reaction) == '🇲':
                await user.remove_roles(ratz)

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import karma
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

            # Game Roles
            global league, hs, fortnite, pubg, tf2, gta, chiv, cs, aoe, civ, rainbow, brawl, ratz, skribble, gmod, apex
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
            skribble = discord.utils.get(guild.roles, id=settings.skribble_role)
            gmod = discord.utils.get(guild.roles, id=settings.gmod_role)
            apex = discord.utils.get(guild.roles, id=settings.apex_role)

            # Group Roles
            global code, boof, max_role, path, poker, dj, snowboard
            code = discord.utils.get(guild.roles, id=settings.code_role)
            boof = discord.utils.get(guild.roles, id=settings.boof_role)
            max_role = discord.utils.get(guild.roles, id=settings.max_role)
            path = discord.utils.get(guild.roles, id=settings.path_role)
            poker = discord.utils.get(guild.roles, id=settings.poker_role)
            dj = discord.utils.get(guild.roles, id=settings.dj_role)
            snowboard = discord.utils.get(guild.roles, id=settings.snowboard_role)

    @client.event
    async def on_raw_reaction_add(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name

            if int(payload.message_id) == settings.groups_message_id:
                if str(reaction) == '🇦':
                    await user.add_roles(code)
                if str(reaction) == '🇧':
                    await user.add_roles(poker)
                if str(reaction) == '🇨':
                    await user.add_roles(snowboard)
                    karma.user_add_karma(user.id, 100)

            if int(payload.message_id) == settings.games_message_id:
                if str(reaction) == '🇦':
                    if payload.user_id != 262677178590822400:
                        await user.add_roles(league)
                if str(reaction) == '🇧':
                    if payload.user_id != 262677178590822400:
                        await user.add_roles(hs)
                if str(reaction) == '🇨':
                    await user.add_roles(fortnite)
                if str(reaction) == '🇩':
                    await user.add_roles(pubg)
                if str(reaction) == '🇪':
                    if payload.user_id != 262677178590822400:
                        await user.add_roles(tf2)
                if str(reaction) == '🇫':
                    await user.add_roles(gta)
                if str(reaction) == '🇬':
                    await user.add_roles(chiv)
                if str(reaction) == '🇭':
                    await user.add_roles(cs)
                if str(reaction) == '🇮':
                    if payload.user_id != 262677178590822400:
                        await user.add_roles(aoe)
                if str(reaction) == '🇯':
                    if payload.user_id != 262677178590822400:
                        await user.add_roles(civ)
                if str(reaction) == '🇰':
                    if payload.user_id != 262677178590822400:
                        await user.add_roles(rainbow)
                if str(reaction) == '🇱':
                    if payload.user_id != 262677178590822400:
                        await user.add_roles(brawl)
                if str(reaction) == '🇲':
                    await user.add_roles(ratz)
                if str(reaction) == '🇳':
                    await user.add_roles(skribble)
                if str(reaction) == '🇴':
                    await user.add_roles(gmod)
                if str(reaction) == '🇵':
                    await user.add_roles(apex)

    @client.event
    async def on_raw_reaction_remove(self, payload):
        if int(payload.channel_id) == settings.game_channel:
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            reaction = payload.emoji.name

            if int(payload.message_id) == settings.games_message_id:
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
                if str(reaction) == '🇳':
                    await user.remove_roles(skribble)
                if str(reaction) == '🇴':
                    await user.remove_roles(gmod)
                if str(reaction) == '🇵':
                    await user.remove_roles(apex)

            if int(payload.message_id) == settings.groups_message_id:
                if str(reaction) == '🇦':
                    await user.remove_roles(code)
                    karma.user_add_karma(user.id, -100)
                if str(reaction) == '🇧':
                    await user.remove_roles(poker)
                if str(reaction) == '🇨':
                    await user.remove_roles(snowboard)

    @client.command(hidden=True)
    @commands.has_role(settings.admin_role_name)
    async def games(self, ctx):
        letters = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵']

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
                                          '🇲 Ratz Instagib\n'
                                          '🇳 Skribble.io\n'
                                          '🇴 G-Mod\n'
                                          '🇵 Apex Legends'
                                          # '🇶'
                                          # '🇷'
                                          # '🇸'
                                          # '🇹'
                                          # '🇺'
                                          # '🇻'
                                          # '🇼'
                                          # '🇾'
                                          # '🇽'
                                          # '🇿'
                              )

        try:
            msg = await ctx.channel.get_message(settings.games_message_id)
            await msg.edit(embed=embed)
        except discord.NotFound:
            msg = await ctx.send(embed=embed)

        for reaction in letters[:len(str(msg.embeds[0].description).split("\n"))]:
            await msg.add_reaction(reaction)

        await ctx.message.delete()

    @client.command(hidden=True)
    @commands.has_role(settings.admin_role_name)
    async def groups(self, ctx):
        letters = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳']

        embed = discord.Embed(color=settings.embed_color, title="Games:",
                              description='🇦 Code Tester\n'
                                          '🇧 Poker\n'
                                          '🇨 Snowboarding\n'
                              )

        try:
            msg = await ctx.channel.get_message(settings.groups_message_id)
            await msg.edit(embed=embed)
        except discord.NotFound:
            msg = await ctx.send(embed=embed)

        for reaction in letters[:len(str(msg.embeds[0].description).split("\n"))]:
            await msg.add_reaction(reaction)

        await ctx.message.delete()


def setup(client):
    client.add_cog(Games(client))

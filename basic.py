#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import aiohttp
import curtime
import asyncio
import discord
import settings
import html5lib
import settings
from bs4 import BeautifulSoup
from discord.ext import commands


class Basic:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Basic...")

    @client.command()
    async def about(self, ctx):
        info = await self.client.application_info()
        embed = discord.Embed(
            title="Info about {}:".format(info.name),
            description="• [Github](https://github.com/Mehvix/synapsBotRW)\n"
                        "• [Trello](https://trello.com/b/CQBT9vag/synapsbot)",
            color=settings.embed_color)
        embed.add_field(name="Creator:", value=info.owner, inline=True)
        embed.add_field(name="Python Version:", value=sys.version.split()[0], inline=True)
        embed.add_field(name="Discord.py Version:", value=discord.__version__, inline=True)
        embed.add_field(name="Client Version:", value=settings.get_version(), inline=True)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @client.command()
    async def trello(self, ctx):
        await ctx.send("Trello Link:\nhttps://trello.com/b/CQBT9vag/synapsbot")

    @client.command()
    async def issue(self, ctx):
        await ctx.send("Please report the issue here:\nhttps://github.com/Mehvix/synapsBotRW/issues")

    @client.command(case_insensitive=True)
    async def ping(self, ctx):
        await ctx.send("I have a latency of `{}` ms".format(str(float(self.client.latency)*1000)[:2]))

    '''
    @client.command(case_insensitive=True)
    async def notation(self, ctx):
        level_role = discord.utils.get(ctx.guild.roles, id=settings.level_role)
        roles_role = discord.utils.get(ctx.guild.roles, id=settings.roles_role)
        groups_role = discord.utils.get(ctx.guild.roles, id=settings.groups_role)
        games_role = discord.utils.get(ctx.guild.roles, id=settings.games_role)
        restriction_role = discord.utils.get(ctx.guild.roles, id=settings.restriction_role)
        level1_role = discord.utils.get(ctx.guild.roles, name="Level 1")

        for member in ctx.message.guild.members:
            if level_role and level_role not in member.roles:
                await member.add_roles(level_role,
                                               roles_role,
                                               groups_role,
                                               games_role,
                                               restriction_role,
                                               level1_role)
                print("Added Notation Roles")
    '''

    @client.event
    async def on_message(self, message):
        if message.author.id != self.client.user.id:
            channel = message.channel

            if "BAD BOT" in message.content.upper():
                await channel.send("Bad Human.")

            if "BOT BROKE" in message.content.upper():
                await channel.send("Please report the issue here:\nhttps://github.com/Mehvix/synapsBotRW/issues")

            if message.content.upper().startswith("GIT "):
                word = message.content.split(" ")
                await channel.send("`git: '{}' is not a git command. See 'git --help'.`".format(" ".join(word[1:])))

            states = ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']
            msg = message.content.upper()
            msg = msg.split(" ")
            if [word for word in msg if word in states]:
                word = [word for word in msg if word in states]
                word = "".join(word)
                search = "https://www.50states.com/facts/{}.htm".format(str(word).lower())
                async with aiohttp.ClientSession() as session:
                    async with session.get(search) as r:
                        text = await r.read()
                        soup = BeautifulSoup(text.decode('utf-8'), 'html5lib')

                        facts = soup.find('ol', attrs={'class': 'stripedList'})
                        facts = facts.text
                        facts = facts.split("\n")
                        await message.channel.send("Speaking of {}, did you know that {}".format(word.title(), random.choice(facts)))

            try:
                if message.author.id != self.client.user.id:
                    print("{}: {} sent '{}' in {}".format(curtime.get_time(), message.author.name, message.content,
                                                          message.channel.name))
            except AttributeError:
                print("{}: {} sent '{}' in {}".format(curtime.get_time(), message.author.name, message.content,
                                                      message.channel.recipient.name))


def setup(client):
    client.add_cog(Basic(client))

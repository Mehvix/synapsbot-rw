#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp
import discord
from discord.ext import commands

import settings


class Typeracer:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Typeracer...")

    @client.command(alias=["type", "racer", "wpm", "typeracer"], description="Gets a users stats on typeracer.com", usage="[username from typeracer.com]", brief="Gets statistics about [username] from typeracer.com")
    async def tr(self, ctx, user):
        user = str(user).lower
        search = "https://data.typeracer.com/users?id=tr:{}".format(user)

        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                if r.status == 200:
                    result = await r.json(content_type='text/html')

                    try:
                        embed = discord.Embed(
                            description="• [Add {0} on Typeracer](https://data.typeracer.com/pit/friend_request?user={0})\n"
                                        "• [View {0}'s Profile](https://data.typeracer.com/pit/profile?user={0})\n• [View {0}'s"
                                        " Game History](https://data.typeracer.com/pit/race_history?user={0}&n=100&startDate=)"
                                        "".format(user), color=settings.embed_color)
                        embed.set_author(name="{}'s Type Racer Stats:".format(user))
                        embed.add_field(name="Name:", value=result["name"] + " " + result["lastName"], inline=True)
                        embed.add_field(name="Country:", value=str(result["country"]).upper(), inline=True)
                        embed.add_field(name="Points:", value=str(result["tstats"]["points"])[:10], inline=True)
                        embed.add_field(name="Level:", value=result["tstats"]["level"], inline=True)
                        embed.add_field(name="Games Won:", value=result["tstats"]["gamesWon"], inline=True)
                        embed.add_field(name="Best WPM:", value=str(result["tstats"]["bestGameWpm"])[:10], inline=True)
                        embed.add_field(name="Average WPM:", value=str(result["tstats"]["wpm"])[:10], inline=True)
                        # embed.add_field(name="Recent WPM:", value=str(result["tstats"]["recentScores"]), inline=True)
                        embed.add_field(name="Average Recent WPM:", value=str(result["tstats"]["recentAvgWpm"])[:10],
                                        inline=True)
                        image = "https://data.typeracer.com/misc/badge?user={}".format(user)
                        embed.set_thumbnail(url=image)

                        await ctx.send(embed=embed)
                    except TypeError:
                        await ctx.send("That user doesn't exist :(")


def setup(client):
    client.add_cog(Typeracer(client))

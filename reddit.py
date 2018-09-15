#!/usr/bin/env python
# -*- coding: utf-8 -*-


import discord
import aiohttp
import settings
from discord.ext import commands


class Reddit:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Reddit...")

    @client.event
    async def on_message(self, message):
        if "reddit.com/r/" and "http" in message.content:
            url = [s for s in str(message.content).split(" ") if "reddit.com/r/" in s]
            url = str("".join(url)) + ".json?limit=1"

            print(url)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    result = await r.json()

            embed = discord.Embed(
                title=str(result[0]['data']['children'][0]['data']['title'])[:256],
                color=settings.embed_color, description="[View Post]({})\n[View Image/Link]({})\n {}".format(
                    "https://old.reddit.com/" + str(result[0]['data']['children'][0]['data']['permalink']),
                    str(result[0]['data']['children'][0]['data']['url']),
                    str(result[0]['data']['children'][0]['data']['selftext'])[:1800]))

            if len(result[0]['data']['children'][0]['data']['selftext']) > 1800:
                embed.set_footer(text="This post was too long to fit. Full version can be found via the 'View "
                                      "Post' button above")

            if 'v.redd.it' in result[0]['data']['children'][0]['data']['url']:
                embed.set_footer(
                    text="NOTE: This is just the thumbnail of video that cannot be played via Discord. You can "
                         "see the video by clicking on 'View Post'")
                embed.set_image(url=result[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url'])
            else:
                if '.jpg' or '.png' or '.jpeg' or '.gif' in result[0]['data']['children'][0]['data']['url']:
                    embed.set_image(url=result[0]['data']['children'][0]['data']['url'])

            embed.add_field(name="Subreddit:", value=result[0]['data']['children'][0]['data']['subreddit_name_prefixed'], inline=True)
            embed.add_field(name="Upvotes:", value=result[0]['data']['children'][0]['data']['score'], inline=True)
            embed.add_field(name="Author:", value=result[0]['data']['children'][0]['data']['author'], inline=True)
            embed.add_field(name="Subreddit Subs:", value=result[0]['data']['children'][0]['data']['subreddit_subscribers'], inline=True)
            # embed.add_field(name="Time Created:", value=result[0]['data']['children'][0]['data']['create_utc'], inline=True) # TODO figure out how to convert this

            await message.channel.send("Here's a preview of that Reddit link!")
            await message.channel.send(embed=embed)


def setup(client):
    client.add_cog(Reddit(client))

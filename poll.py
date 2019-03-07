#!/usr/bin/env python
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

import settings

vote_phase = 0


class Poll(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Poll...")

    @commands.command()
    async def poll(self, ctx, question, *options: str):
        if question is None:
            print("user had no question")
        if len(options) <= 1:
            await ctx.send('Your poll should be formatted like `.poll question option1, option2, option3,` etc.')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things.\nMake sure your poll is fomatted like '
                           '`.poll question option1, option2, option3,` etc.')
            return

        if "?" not in question:
            question += "?"

        if len(options) == 2 and str(options[0]).upper() == 'yes' and str(options[1]).upper() == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']

        description = []
        for x, option in enumerate(options):
            description += '\n {}  {}'.format(reactions[x], str(option).title())

        embed = discord.Embed(title=str(question).title(), color=settings.embed_color, description=''.join(description))
        embed.set_author(name="Created by " + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        react_message = await ctx.send(embed=embed)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)


def setup(client):
    client.add_cog(Poll(client))

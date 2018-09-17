#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import zalgo
import karma
import random
import string
import aiohttp
import discord
import asyncio
import curtime
import settings
from discord.ext import commands
from urbandictionary_top import udtop


class Verified:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Verified...")

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def ud(self, ctx, *word: str):
        term = " ".join(word)
        term_link = term.replace(" ", "%20")
        if term.upper() == "MAGGIE":
            embed = discord.Embed(title="Definition Page", url="https://goo.gl/j2DX9N", color=settings.embed_color)
            embed.set_author(name="Definition for Maggie", url="https://goo.gl/j2DX9N")
            embed.add_field(name="Definition 📚", value="Girl with YUUUG milkers. Doesn't need a coat",
                            inline=False)
            embed.add_field(name="Example 💬",
                            value="Maggie's got such big fun-fun milk bags, she doesn't need a coat! "
                                  "-Aidan Witkovsky 2018",
                            inline=True)
            await ctx.message.channel.send(embed=embed)
        else:
            try:
                term_def = udtop(term)

                embed = discord.Embed(
                    title="Definition Page", url="https://www.urbandictionary.com/define.php?term={}".format(term_link),
                    color=settings.embed_color)
                embed.set_author(name="Definition for {}".format(str(term).title()))
                embed.add_field(name="📚 Definition ", value=term_def.definition[:1023], inline=False)
                embed.add_field(name="💬 Example ", value=term_def.example[:1023], inline=True)
                await ctx.message.channel.send(embed=embed)
            except udtop.TermNotFound as error:
                await ctx.message.channel.send("ERROR: `{}`\n However, you can add your own here: "
                                               "https://www.urbandictionary.com/add.php?word={}".
                                               format(error, term_link))

    @client.command()  # TODO work on this
    @commands.has_role(settings.verified_role_name)
    async def price(self, ctx, coin: str):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coinmarketcap.com/v1/ticker/") as r:
                result = await r.json()
        coin = "".join(coin)
        print(result)
        print(coin)
        x = 0
        while x != 999:
            data = result[int(x)]
            if coin in data:
                x = 999
                return
            x += 1
        print(data)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def profile(self, ctx):
        search = "https://discordapp.com/users/{}/profile".format(ctx.message.author.id)
        # this is going to take a lot more webscraping knowledge than I have because you have to log into discord...
        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                if r.status == 200:
                    result = await r.json()
                    await ctx.message.channel.send(result)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def zalgo(self, ctx, *target):
        target = " ".join(target)
        intensity = {"up": 5, "mid": 5, "down": 5}
        await ctx.message.channel.send(zalgo.zalgo(target, intensity))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def uptime(self, ctx):
        await ctx.message.channel.send("The bot has been live for `{}` {}".format(curtime.uptime(),
                                                                                  settings.random_clock()))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def announce(self, ctx, role: discord.Role, *message: str):
        print(role.members, message)
        message = " ".join(message)
        for member in role.members:
            embed = discord.Embed(
                color=settings.embed_color, description=message)
            embed.set_author(name="{} sent an announcement to {} others in {}".format(
                    ctx.message.author.name, len(role.members), role.name), icon_url=ctx.message.author.avatar_url)
            await member.send(embed=embed)



    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def sam(self, ctx):
        fp = random.choice(os.listdir("media/sams"))
        await ctx.message.channel.send(file=discord.File("media/sams/{}".format(fp)))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def aidan(self, ctx):
        fp = random.choice(os.listdir("media/aidans"))
        await ctx.message.channel.send(file=discord.File("media/aidans/{}".format(fp)))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def apu(self, ctx):
        fp = random.choice(os.listdir("media/apus"))
        await ctx.message.channel.send(file=discord.File("media/apus/{}".format(fp)))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def bear(self, ctx):
        fp = random.choice(os.listdir("media/bears"))
        await ctx.message.channel.send(file=discord.File("media/bears/{}".format(fp)))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def cat(self, ctx):
        search = "https://nekos.life/api/v2/img/meow"

        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                if r.status == 200:
                    result = await r.json()
                    await ctx.message.channel.send(result['url'])

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def dog(self, ctx):
        search = "https://dog.ceo/api/breeds/image/random"

        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                if r.status == 200:
                    result = await r.json()
                    await ctx.message.channel.send(result['message'])

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def serverinfo(self, ctx):  # make this admin
        online = 0
        for i in ctx.message.guild.members:
            if str(i.status) == "online" or str(i.status) == "idle" or str(i.status) == "dnd":
                online += 1

        ban_list = await ctx.message.guild.bans()
        user = [user for user in ban_list]

        em = discord.Embed(color=settings.embed_color, title="Server Info:")
        em.add_field(name="Server Name:", value=ctx.message.guild.name)
        em.add_field(name="Server ID:", value=ctx.message.guild.id)
        em.add_field(name="Owner:", value=ctx.message.guild.owner, inline=False)
        em.add_field(name="Members:", value=ctx.message.guild.member_count)
        em.add_field(name="Members Online:", value=online)
        em.add_field(name="Region:", value=ctx.message.guild.region)
        em.add_field(name="Verification Level:", value=str(ctx.message.guild.verification_level).capitalize())
        em.add_field(name="Highest Ranking Role:", value=ctx.message.guild.role_hierarchy[0])
        em.add_field(name="Number of Roles:", value=str(len(ctx.message.guild.roles)))
        em.add_field(name="Number of Channels:", value=str(len(ctx.message.guild.channels)))
        em.add_field(name="Number of Text Channels:", value=str(len(ctx.message.guild.text_channels)))
        em.add_field(name="Number of Bans:", value=str(len(user)))
        em.add_field(name="Custom Emotes:", value=str(len(ctx.message.guild.emojis)))
        em.add_field(name="Time Created:", value=str(ctx.message.guild.created_at).split(".")[0])
        em.add_field(name="AFK Time:", value="{} seconds".format(ctx.message.guild.afk_timeout))
        em.add_field(name="AFK Channel:", value=ctx.message.guild.afk_channel)
        em.add_field(name="Voice Client:", value=ctx.message.guild.voice_client)
        em.add_field(name="Icon URL", value=ctx.message.guild.icon_url)
        em.set_thumbnail(url=ctx.message.guild.icon_url)
        em.set_author(name="\u200b")
        await ctx.message.channel.send(embed=em)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def emotes(self, ctx):
        emojis = [str(x) for x in ctx.message.guild.emojis]
        await ctx.message.channel.send(" ".join(emojis))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def beta(self, ctx):
        user = self.client.get_user(196355904503939073)
        user.send("Hey <@!196355904503939073>, <@{}> wants beta access.\nType `.allow` to send them an invite".format(
            ctx.author.id))

        x = 0
        while x != 1:
            msg = await self.client.wait_for("message")
            if 196355904503939073 == msg.author.id and msg.content.upper() == '.ALLOW':
                x = 1
            else:
                x = 0

        testinvite = settings.get_json('testserver_invite.json')
        print(testinvite)
        invite = testinvite.get("invite")
        await ctx.author.send("You've been accepted! {}".format(invite))
        await ctx.message.channel.send(
            "<@{}> was accepted into the beta testing server! :tada:\nYou can apply via the `.beta` command.".format(
                ctx.message.author.id))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def copypasta(self, ctx):
        search = "https://www.reddit.com/r/copypasta/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json()
                    if result[0]['data']['children'][0]['data']['author'] == "AutoModerator" or \
                            result[0]['data']['children'][0]['data']['pinned'] == "true":
                        print("Post was automodpost, skipping")
                        pass
                    else:
                        c = 1

        embed = discord.Embed(
            title=str(result[0]['data']['children'][0]['data']['title'])[:256],
            color=settings.embed_color,
            description="[View Post]({})\n {}".format(
                "https://old.reddit.com" + str(result[0]['data']['children'][0]['data']['permalink']),
                str(result[0]['data']['children'][0]['data']['selftext'])[:1800]))

        if len(result[0]['data']['children'][0]['data']['selftext']) > 1800:
            embed.set_footer(text="This post was too long to fit. Full version can be found via the 'View "
                                  "Post' button above")

        await ctx.message.channel.send(embed=embed)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def emojipasta(self, ctx):
        search = "https://www.reddit.com/r/emojipasta/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json()
                    if result[0]['data']['children'][0]['data']['author'] == "AutoModerator" or \
                            result[0]['data']['children'][0]['data']['pinned'] == "true":
                        print("Post was automodpost, skipping")
                        pass
                    else:
                        c = 1

        print(search)

        embed = discord.Embed(
            title=str(result[0]['data']['children'][0]['data']['title'])[:256],
            color=settings.embed_color, description="[View Post]({})\n {}".format(
                'https://old.reddit.com' + str(result[0]['data']['children'][0]['data']['permalink']),
                str(result[0]['data']['children'][0]['data']['selftext'])[:1800]))

        if 'v.redd.it' in result[0]['data']['children'][0]['data']['url']:
            embed.set_footer(text="NOTE: This is just the thumbnail of video that cannot be played via Discord. You can "
                                  "see the video by clicking on 'View Post'")
            embed.set_image(url=result[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url'])
        else:
            if '.jpg' or '.png' or '.jpeg' or '.gif' in result[0]['data']['children'][0]['data']['url']:
                embed.set_image(url=result[0]['data']['children'][0]['data']['url'])

        if len(result[0]['data']['children'][0]['data']['selftext']) > 1800:
            embed.set_footer(text="This post was too long to fit. Full version can be found via the 'View "
                                  "Post' button above")

        await ctx.message.channel.send(embed=embed)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def coaxed(self, ctx):
        search = "https://www.reddit.com/r/coaxedintoasnafu/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json()
                    if result[0]['data']['children'][0]['data']['author'] == "AutoModerator" or \
                            result[0]['data']['children'][0]['data']['pinned'] == "true":
                        print("Post was automodpost, skipping")
                        pass
                    else:
                        c = 1

        embed = discord.Embed(
            title=str(result[0]['data']['children'][0]['data']['title'])[:256],
            color=settings.embed_color, description="[View Post]({})\n[View Image/Link]({})\n {}".format(
                "https://old.reddit.com" + str(result[0]['data']['children'][0]['data']['permalink']),
                str(result[0]['data']['children'][0]['data']['url']),
                str(result[0]['data']['children'][0]['data']['selftext'])[:1800]))

        if len(result[0]['data']['children'][0]['data']['selftext']) > 1800:
            embed.set_footer(text="This post was too long to fit. Full version can be found via the 'View "
                                  "Post' button above")

        if 'v.redd.it' in result[0]['data']['children'][0]['data']['url']:
            embed.set_footer(text="NOTE: This is just the thumbnail of video that cannot be played via Discord. You can "
                                  "see the video by clicking on 'View Post'")
            embed.set_image(url=result[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url'])
        else:
            if '.jpg' or '.png' or '.jpeg' or '.gif' in result[0]['data']['children'][0]['data']['url']:
                embed.set_image(url=result[0]['data']['children'][0]['data']['url'])

        await ctx.message.channel.send(embed=embed)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def hmmm(self, ctx):
        search = "https://www.reddit.com/r/hmmm/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json()
                    if result[0]['data']['children'][0]['data']['author'] == "AutoModerator" or \
                            result[0]['data']['children'][0]['data']['pinned'] == "true":
                        print("Post was automodpost, skipping")
                        pass
                    else:
                        c = 1

        embed = discord.Embed(
            title=str(result[0]['data']['children'][0]['data']['title'])[:256],
            color=settings.embed_color, description="[View Post]({})\n[View Image/Link]({})\n {}".format(
                "https://old.reddit.com" + str(result[0]['data']['children'][0]['data']['permalink']),
                str(result[0]['data']['children'][0]['data']['url']),
                str(result[0]['data']['children'][0]['data']['selftext'])[:1800]))

        if len(result[0]['data']['children'][0]['data']['selftext']) > 1800:
            embed.set_footer(text="This post was too long to fit. Full version can be found via the 'View "
                                  "Post' button above")

        if 'v.redd.it' in result[0]['data']['children'][0]['data']['url']:
            embed.set_footer(text="NOTE: This is just the thumbnail of video that cannot be played via Discord. You can "
                                  "see the video by clicking on 'View Post'")
            embed.set_image(url=result[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url'])
        else:
            if '.jpg' or '.png' or '.jpeg' or '.gif' in result[0]['data']['children'][0]['data']['url']:
                embed.set_image(url=result[0]['data']['children'][0]['data']['url'])

        await ctx.message.channel.send(embed=embed)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def whois(self, ctx, user: discord.Member):
        full_user_name = "{}#{}".format(user.name, user.discriminator)
        user_join_date = str(user.joined_at).split('.', 1)[0]
        user_created_at_date = str(user.created_at).split('.', 1)[0]
        avatar = user.avatar_url if user.avatar else user.default_avatar_url

        embed = discord.Embed(color=settings.embed_color)
        embed.set_author(name="User Info")
        embed.add_field(name="Username:", value=full_user_name)
        embed.add_field(name="Nickname:", value=user.nick)
        embed.add_field(name="User ID:", value=user.id)
        embed.add_field(name="Joined the server on:", value=user_join_date[:10])
        embed.add_field(name="Account Created on:", value=user_created_at_date[:10])
        embed.add_field(name="Top Role:", value=user.top_role)
        embed.add_field(name="User Status:", value=str(user.status).title())
        embed.add_field(name="User Game:", value=user.game)
        embed.add_field(name="User Custom Name:", value=user.nick)
        embed.add_field(name="User Role Color:", value=user.color)

        # profile = await self.client.get_user_profile(user.id)
        # print(profile.premium)

        embed.add_field(name="User Role Color:", value=user.color)
        if len(user.roles) > 1:  # TIL @everyone is a role that is assigned to everyone but hidden
            embed.add_field(name="User Top Role (Level):", value=user.top_role)
        else:
            embed.add_field(name="User Top Role (Level):", value="User has no roles")
        embed.add_field(name="User Avatar URL", value=avatar)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.message.channel.send(embed=embed)

    @client.command()  # TODO add bot emote to this
    @commands.has_role(settings.verified_role_name)
    async def banlist(self, ctx):
        bans = await ctx.message.guild.bans()
        if not bans:
            embed = discord.Embed(title="Ban List", description="This server doesn't have anyone banned (yet)", color=settings.embed_color)
            await ctx.message.channel.send(embed=embed)
        else:
            pretty_list = ["• <@{0.id}> ({0.name}#{0.discriminator})".format(entry.user) for entry in bans]
            embed = discord.Embed(color=settings.embed_color, title="Ban List", description="\n".join(pretty_list))
            await ctx.message.channel.send(embed=embed)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def createinvite(self, ctx):
        invite = await ctx.channel.create_invite(
            temporary=True, unique=True, reason="{} ({}) created this invite via .createinvite".format(
                ctx.message.author.name, ctx.message.author.id))
        await ctx.message.channel.send(invite.url) # TODO add more info to this

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def oujia(self, ctx, *question):
        question = "".join(question)
        if question != "":
            outcomes = ["Odds aren't that good" "It is certain.", "It is decidedly so.", "Without a doubt.",
                        "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
                        "Yes.", "Signs point to yes.", "Don't count on it.", "My reply is no.", "My sources say no",
                        "Outlook not so good.", "Very doubtful."]
            letters = list(string.printable)
            choice = "".join(random.choices(outcomes))
            nums = len(choice)
            bleh = []
            z = 0
            position = 0

            while z != nums:  # generate a str with same length as outcome with random characters
                bleh.append("".join(random.choices(letters)))
                z += 1

            msg = await ctx.send("".join(bleh))
            while position != nums:
                times = 0
                while times != 1:  # fake hardsolving
                    bleh.insert(position, "".join(random.choices(letters)))
                    bleh.pop(position + 1)
                    times = random.randint(1, 2)  # this could be at '1,5' or high but discord rate limits are very restrictive
                    await msg.edit(content="".join(bleh))
                bleh.insert(position, str(choice)[position])
                bleh.pop(position + 1)
                position += 1
        else:
            await ctx.send("You need a question!")

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def roulette(self, ctx, *args: str):
        try:
            args = " ".join(args)
            args = args.split(" ")
            outcome = str(args[0]).lower()
        except (IndexError, ValueError, AttributeError):
            await ctx.message.channel.send(
                "You need to format your message such as \n`.roulette [odd/even/zero] [amount of karma <250 and > 10]`")
            return

        print(outcome)

        if "help" in outcome:  # TODO update this to make it look/read better
            embed = discord.Embed(title="Roulette Help:", description="Type ", color=settings.embed_color)
            await ctx.message.channel.send(embed=embed)
            return

        if "outcome" in outcome:
            with open('roulette_outcomes.json', 'r') as fp:
                outcomes = json.load(fp)
            odd_total = outcomes['odd']
            even_total = outcomes['even']
            zero_total = outcomes['zero']
            total_total = outcomes['total']

            outcomes_list = [odd_total, even_total, zero_total]
            total = sum(outcomes_list)
            embed = discord.Embed(title="\u200b", color=settings.embed_color)
            embed.set_author(name="Roulette Outcomes 📊")
            embed.add_field(name="Total number of times 'spun'", value=total, inline=True)
            embed.add_field(name="Total Karma Bet", value=total_total, inline=False)
            embed.add_field(name="Odd", value=odd_total, inline=True)
            embed.add_field(name="Even", value=even_total, inline=True)
            embed.add_field(name="Zero", value=zero_total, inline=True)
            await ctx.message.channel.send(embed=embed)
            return

        amount = int(args[1])

        outcomes = ['odd', 'even', 'zero']  # TODO add more outcome options
        if outcome not in outcomes:
            print("1" + outcome)
            await ctx.message.channel.send(
                "You need to format your message such as \n`.roulette [odd/even/zero] [amount of karma <250 and > 10]`")
            return

        if 10 > amount > 250:
            print('2')
            await ctx.message.channel.send(
                "You need to format your message such as \n`.roulette [odd/even/zero] [amount of karma < 250 and > 10]`")
            return

        if amount > karma.get_karma(ctx.message.author.id):
            await ctx.message.channel.send(
                "You only have `{}` karma, which isn't enough to bet that much".format(karma.get_karma(ctx.message.author.id)))
            return

        with open('roulette_outcomes.json', 'r') as fp:
            outcomes = json.load(fp)
        outcomes['total'] += amount
        with open('roulette_outcomes.json', 'w') as fp:
            json.dump(outcomes, fp, sort_keys=True, indent=4)

        karma.user_add_karma(ctx.message.author.id, -amount)

        spin = random.randint(0, 36)

        msg = await ctx.message.channel.send("It landed on `{}`!".format(spin))

        if spin == 0:
            await msg.pin()
            if outcome == "zero":
                karma.user_add_karma(ctx.message.author.id, amount * 14)
                await ctx.message.channel.send("You won! :tada:\nYour new karma total is `{}`".format(
                    karma.get_karma(ctx.message.author.id)))
            else:
                await ctx.message.channel.send("You lost!\nYour new karma total is `{}`".format(
                    karma.get_karma(ctx.message.author.id)))

            return
        if spin % 2 == 0:
            real_outcome = "even"
        else:
            real_outcome = "odd"
        with open('roulette_outcomes.json', 'r') as fp:
            outcomes = json.load(fp)
        outcomes[real_outcome] += 1
        with open('roulette_outcomes.json', 'w') as fp:
            json.dump(outcomes, fp, sort_keys=True, indent=4)

        if real_outcome == outcome:
            karma.user_add_karma(ctx.message.author.id, amount*2)
            await ctx.message.channel.send("You won! :tada:\nYour new karma total is `{}`".format(
                karma.get_karma(ctx.message.author.id)))
        else:
            await ctx.message.channel.send("You lost!\nYour new karma total is `{}`".format(
                karma.get_karma(ctx.message.author.id)))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def bannedwords(self, ctx):
        banned_words = settings.get_json("banned_words.json")
        lower = [item.lower() for item in banned_words]

        await ctx.message.channel.send("**Banned Words List:** \n• {}".format("\n• ".join(lower)))

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def jpeg(self, ctx, *args):
        pass

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def generate(self, ctx, *args):
        args = " ".join(args)
        emote = args[0]
        emote = " ".join(emote)
        text = args[1:]
        text = "".join(text)

        await ctx.send(str(text).replace(" ", " " + emote) + " " + emote)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def leaderboard(self, ctx, *kind):
        kind = " ".join(kind)
        with open("users.json") as fp:
            file = json.load(fp)

        if "level" in kind.lower():
            type_new = "level"
            word = "is"
        else:
            type_new = "karma"
            word = "has"

        karma_leaderboard = sorted(file, key=lambda x: file[x].get(type_new, 0), reverse=True)
        msg = ''
        for number, user in enumerate(karma_leaderboard):
            msg += '__{}__. **{}** {} `{}` {} \n'.format(
                number + 1, file[user]['name'], word, file[user].get(type_new, 0), type_new)
        await ctx.send(msg)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def invites(self, ctx):
        server = ctx.message.guild
        active_invites = await server.invites()

        revoked_invites = ['~~{0.code}: `{0.channel}` created by `{0.inviter}`~~ '.format(x) for x in active_invites if
                           x.revoked]
        unlimited_invites = ['[`{0.code}`]({0.url}): `{0.channel}` created by `{0.inviter}`'.format(x) for x in
                             active_invites if x.max_age == 0 and x not in revoked_invites]
        limited_invites = ['[`{0.code}`]({0.url}): `{0.channel}` created by `{0.inviter}`'.format(x) for x in
                           active_invites if x.max_age != 0 and x not in revoked_invites]

        embed = discord.Embed(title='__Invite links for {0.name}__'.format(server),
                              color=ctx.message.author.color)
        if unlimited_invites:
            embed.add_field(name='Unlimited Invites ({})'.format(len(unlimited_invites)),
                            value='\n'.join(unlimited_invites[:5]))
        if limited_invites:
            embed.add_field(name='Temporary/Finite Invites ({})'.format(len(limited_invites)),
                            value='\n'.join(limited_invites))
        if revoked_invites:
            embed.add_field(name='Revoked Invites ({})'.format(len(revoked_invites)), value='\n'.join(revoked_invites))
        await ctx.send(embed=embed)

    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def insult(self, ctx, user: discord.Member):
        insults = settings.get_json("insults.json")

        if user == self.client.user:
            await ctx.message.channel.send(
                "How original. No one else had thought of trying to get the bot to insult itself. I applaud your "
                "creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any "
                "conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an "
                "actual conversation with.")
            return
        await ctx.message.channel.send("<@{}>, {}".format(user.id, random.choice(insults)))


def setup(client):
    client.add_cog(Verified(client))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import json
import random
import string
import aiohttp
import pyqrcode
from urbandictionary_top import udtop

import discord
from discord.ext import commands

import zalgo
import karma
import curtime
import settings


image_files = ['.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif',
               '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm']


class Verified:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Verified...")

    @client.command(aliases=["urban", "dictionary", "definition", "define"], description="Finds the Urban Dictionary definition/example of a word", usage="[word]", brief="Gets the Urban Dictionary definition and examples of a [word]")
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

    '''
    @client.command(description="TODO", usage="[]", brief="TODO")
    @commands.has_role(settings.verified_role_name)
    async def profile(self, ctx):
        search = "https://discordapp.com/users/{}/profile".format(ctx.message.author.id)
        # this is going to take a lot more webscraping knowledge than I have because you have to log into discord...
        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                if r.status == 200:
                    result = await r.json(content_type='application/json')
                    await ctx.message.channel.send(result)
    '''

    @client.command(description="Makes text look whack", usage="[word/sentence]", brief="Adds zalgo effect to [word/sentecne]")
    @commands.has_role(settings.verified_role_name)
    async def zalgo(self, ctx, *target):
        target = " ".join(target)
        intensity = {"up": 5, "mid": 5, "down": 5}
        await ctx.message.channel.send(zalgo.zalgo(target, intensity))

    @client.command(aliases=["up"], description="Returns how long the bot has been live", brief="Returns how long the bot has been live")
    @commands.has_role(settings.verified_role_name)
    async def uptime(self, ctx):
        await ctx.message.channel.send("The bot has been live for `{}` {}".format(curtime.uptime(),
                                                                                  settings.random_clock()))

    @client.command(description="Used to DM everyone in a role", usage="[role] [message]", brief="Sends everyone who has [role] the [message]. This should be used for game night/etc.")
    @commands.has_role(settings.verified_role_name)
    async def announce(self, ctx, role: discord.Role, *message: str):
        print(role.members, message)
        message = " ".join(message)
        for member in role.members:
            embed = discord.Embed(
                color=settings.embed_color, description=message)
            embed.set_author(name="{} sent an announcement to you because you are a member of the group '{}''".format(
                    ctx.message.author.name, role.name), icon_url=ctx.message.author.avatar_url)
            await member.send(embed=embed)

    @client.command(description="Gets a random Sammy pic", brief="Gets a random Sammy pic")
    @commands.has_role(settings.verified_role_name)
    async def sam(self, ctx):
        fp = random.choice(os.listdir("media/sams"))
        await ctx.message.channel.send(file=discord.File("media/sams/{}".format(fp)))

    @client.command(description="Gets a random picture of Aidan", brief="Gets a random picture of Aidan")
    @commands.has_role(settings.verified_role_name)
    async def aidan(self, ctx):
        fp = random.choice(os.listdir("media/aidans"))
        await ctx.message.channel.send(file=discord.File("media/aidans/{}".format(fp)))

    @client.command(aliases=["fren", "frens"],description="Gets a random Apu", brief="Gets a random Apu")
    @commands.has_role(settings.verified_role_name)
    async def apu(self, ctx):
        fp = random.choice(os.listdir("media/apus"))
        await ctx.message.channel.send(file=discord.File("media/apus/{}".format(fp)))

    @client.command(description="Gets a random Bear gif", brief="Gets a random Bear gif")
    @commands.has_role(settings.verified_role_name)
    async def bear(self, ctx):
        fp = random.choice(os.listdir("media/bears"))
        await ctx.message.channel.send(file=discord.File("media/bears/{}".format(fp)))

    @client.command(description="Gets a random Cat picture", brief="Gets a random Cat picture")
    @commands.has_role(settings.verified_role_name)
    async def cat(self, ctx):
        search = "https://nekos.life/api/v2/img/meow"

        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                if r.status == 200:
                    result = await r.json(content_type='application/json')
                    await ctx.message.channel.send(result['url'])

    @client.command(description="Gets a random Dog picture", brief="Gets a random Dog picture")
    @commands.has_role(settings.verified_role_name)
    async def dog(self, ctx):
        search = "https://dog.ceo/api/breeds/image/random"

        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                if r.status == 200:
                    result = await r.json(content_type='application/json')
                    await ctx.message.channel.send(result['message'])

    @client.command(description="Gets Information about the server", brief="")
    @commands.has_role(settings.verified_role_name)
    async def serverinfo(self, ctx):
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
        # em.add_field(name="Highest Ranking Role:", value=ctx.message.guild.role_hierarchy[0])
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

    @client.command(aliases=["emojis", "emotelist", "emojilist"], description="Returns all emotes in the server", brief="Returns all emotes in the server")
    @commands.has_role(settings.verified_role_name)
    async def emotes(self, ctx):
        emojis = [str(x) for x in ctx.message.guild.emojis]
        await ctx.message.channel.send(" ".join(emojis))

    @client.command(description="Asks access to testing server", brief="Asks access to testing server")
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

    @client.command(description="Random copypasta", brief="Gets a random post from /r/copypastas")
    @commands.has_role(settings.verified_role_name)
    async def copypasta(self, ctx):
        search = "https://www.reddit.com/r/copypasta/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json(content_type='application/json')
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

    @client.command(description="Info about an invite", usage="[invite URL]", brief="Info about an invite")
    @commands.has_role(settings.verified_role_name)
    async def inviteinfo(self, ctx, invite: discord.Invite):
        invite.max_age = invite.max_age if invite.max_age is not None else 0
        m, s = divmod(invite.max_age, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        w, d = divmod(d, 7)
        em = discord.Embed(title="Info for Invite {}:".format(invite.code), color=settings.embed_color)
        try:
            em.set_thumbnail(url=invite.guild.icon_url)
        except AttributeError:
            pass
        em.add_field(name="Server:", value="{} (ID: {})".format(invite.guild.name, invite.guild.id), inline=False)
        em.add_field(name="Channel:", value="#{} (ID: {})".format(invite.channel.name, invite.channel.id), inline=False)
        em.add_field(name="Inviter:", value="{} (ID: {})".format(invite.inviter.name, invite.inviter.id), inline=False)
        em.add_field(name="Created At:", value=str(invite.created_at), inline=True)
        em.add_field(name="Temporary?:", value=str(invite.temporary), inline=True)
        em.add_field(name="Uses:", value=invite.uses, inline=True)
        em.add_field(name="Max Uses:", value=invite.max_uses if invite.max_uses else "Infinite", inline=True)
        em.add_field(name="Expires In:", value=f"{int(w)}w : {int(d)}d : {int(h)}h : {int(m)}m : {int(s)}s" if
        invite.max_age > 0 else "Never")
        await ctx.send(embed=em)

    @client.command(aliases=["transfer"], description="Lets users to give others karma", usage="[@user] [amount]", brief="Gives [@user] [amount] of karma from your account")
    @commands.has_role(settings.verified_role_name)
    async def tradekarma(self, ctx, target: discord.Member, amount: int):
        if amount < 0:
            await ctx.send("You cannot give negative karma")
            return

        if amount > karma.get_karma(ctx.author.id):
            await ctx.send("You cannot trade more karma than you have")
            return

        karma.user_add_karma(target.id, amount)
        karma.user_add_karma(ctx.author.id, -amount)
        await ctx.message.channel.send(
            "You traded <@{}> `{}` karma. They now have a total of `{}` karma and you have `{}`".format(
                target.id, amount, karma.get_karma(target.id), karma.get_karma(ctx.author.id)))

    @client.command(description="Random emojipasta", brief="Gets a random post from /r/emojipastas")
    @commands.has_role(settings.verified_role_name)
    async def emojipasta(self, ctx):
        search = "https://www.reddit.com/r/emojipasta/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json(content_type='application/json')
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
            embed.set_footer(text="NOTE: This is just the thumbnail of video that cannot be played via Discord. You can"
                                  " see the video by clicking on 'View Post'")
            embed.set_image(url=result[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url'])
        else:
            if any(word in str(result[0]['data']['children'][0]['data']['url']).rsplit('/', 1)[1] for word in image_files):
                embed.set_image(url=result[0]['data']['children'][0]['data']['url'])

        if len(result[0]['data']['children'][0]['data']['selftext']) > 1800:
            embed.set_footer(text="This post was too long to fit. Full version can be found via the 'View "
                                  "Post' button above")

        await ctx.message.channel.send(embed=embed)

    @client.command(description="Random coaxed", brief="Gets a random post from /r/caoxedintoasnafu")
    @commands.has_role(settings.verified_role_name)
    async def coaxed(self, ctx):
        search = "https://www.reddit.com/r/coaxedintoasnafu/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json(content_type='application/json')
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
            if any(word in str(result[0]['data']['children'][0]['data']['url']).rsplit('/', 1)[1] for word in image_files):
                embed.set_image(url=result[0]['data']['children'][0]['data']['url'])

        await ctx.message.channel.send(embed=embed)

    @client.command(aliases=["hmm", "hmmmm"], description="Random hmmm", brief="Gets a random post from /r/hmmm")
    @commands.has_role(settings.verified_role_name)
    async def hmmm(self, ctx):
        search = "https://www.reddit.com/r/hmmm/random/.json?limit=1"
        c = 0
        while c != 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json(content_type='application/json')
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
            if any(word in str(result[0]['data']['children'][0]['data']['url']).rsplit('/', 1)[1] for word in image_files):
                embed.set_image(url=result[0]['data']['children'][0]['data']['url'])

        await ctx.message.channel.send(embed=embed)

    @client.command(aliases=["user", "info", "profile"], description="Gives info about a user", usage="[@user]", brief="Gives info about [@user]")
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
        embed.add_field(name="Highest Role:", value=user.top_role)
        embed.add_field(name="Status:", value=str(user.status).title())
        embed.add_field(name="Game/Activity:", value=user.activity.name)
        embed.add_field(name="Custom Name:", value=user.nick)
        embed.add_field(name="Role Color:", value=user.color)
        if len(user.roles) > 1:  # TIL @everyone is a role that is assigned to everyone but hidden
            embed.add_field(name="User Top Role (Level):", value=user.top_role)
        else:
            embed.add_field(name="User Top Role (Level):", value="User has no roles")
        embed.add_field(name="User Avatar URL", value=avatar)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.message.channel.send(embed=embed)

    @client.command(aliases=["bans", "banslist"], description="Lists everyone banned from the server", brief="Lists everyone banned from the server")
    @commands.has_role(settings.verified_role_name)
    async def banlist(self, ctx):
        bans = await ctx.message.guild.bans()
        if not bans:
            embed = discord.Embed(title="Ban List", description="This server doesn't have anyone banned (yet)", color=settings.embed_color)
            await ctx.message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="🔨 Ban List:", color=settings.embed_color)
            await ctx.message.channel.send(embed=embed)
            for entry in bans:
                embed = discord.Embed(color=settings.embed_color)
                embed.set_thumbnail(url=entry.user.avatar_url)
                embed.add_field(name="{}{}#{} [{}]".format("🤖 " if entry.user.bot is True else "",
                                                           entry.user.name,
                                                           entry.user.discriminator,
                                                           entry.user.id),
                                value="Reason: {}".format(entry.reason), inline=False)
                await ctx.message.channel.send(embed=embed)

            await ctx.message.channel.send(embed=embed)

    @client.command(aliases=["invite"], description="Creates an invite for the server", brief="Creates an invite for the server")
    @commands.has_role(settings.verified_role_name)
    async def createinvite(self, ctx):
        invite = await ctx.channel.create_invite(
            temporary=True, reason="{} ({}) created this invite via .createinvite".format(
                ctx.message.author.name, ctx.message.author.id))
        await ctx.message.channel.send(invite.url)

        # QR code
        url = pyqrcode.create(invite.url)
        with open('invite.png', 'wb') as fstream:
            url.png(fstream, scale=3)

        buffer = io.BytesIO()
        url.png(buffer)

        await ctx.send(file=discord.File("invite.png"))

    @client.command(aliases=["8ball"], description="Answers questions 110% accurately", usage="[question]", brief="Answers [questions]")
    @commands.has_role(settings.verified_role_name)
    async def oujia(self, ctx, *question):
        question = "".join(question)
        if question != "":
            outcomes = ["Odds aren't that good" "It is certain.", "It is decidedly so.", "Without a doubt.",
                        "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
                        "Yes.", "Signs point to yes.", "Don't count on it.", "My reply is no.", "My sources say no",
                        "Outlook not so good.", "Very doubtful." , "Yummy."]
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
                    times = random.randint(1, 2)  # this could be at '(1,5)' or high but discord rate limits are very restrictive
                    await msg.edit(content="".join(bleh))
                bleh.insert(position, str(choice)[position])
                bleh.pop(position + 1)
                position += 1
        else:
            await ctx.send("You need a question!")

    @client.command(aliases=["outcomes"], description="Roulette outcomes", brief="Roulette outcomes")
    @commands.has_role(settings.verified_role_name)
    async def roulette_outcomes(self, ctx):
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

    @client.command(aliases=["r", "roulete", "roullete", "bet"], description="There is little time, do .roulette help", usage="[odd/even/zero] [amount of karma < 250 and > 10]", brief="Lets you bet [amount of karma] on an outcome, [odd/even/zero] ")
    @commands.has_role(settings.verified_role_name)
    async def roulette(self, ctx, outcome: str, *amount):
        if "outcome" in outcome:
            with open('roulette_outcomes.json', 'r') as fp:
                outcomes = json.load(fp)
            odd_total = outcomes['odd']
            even_total = outcomes['even']
            zero_total = outcomes['zero']
            total_total = outcomes['total']

            outcomes_list = [odd_total, even_total, zero_total]
            total = sum(outcomes_list)
            embed = discord.Embed(color=settings.embed_color)
            embed.set_author(name="Roulette Outcomes 📊")
            embed.add_field(name="Total number of times 'spun'", value=total, inline=True)
            embed.add_field(name="Total Karma Bet", value=total_total, inline=False)
            embed.add_field(name="Odd", value=odd_total, inline=True)
            embed.add_field(name="Even", value=even_total, inline=True)
            embed.add_field(name="Zero", value=zero_total, inline=True)
            await ctx.message.channel.send(embed=embed)
            return

        outcomes = ['odd', 'even', 'zero']
        if outcome not in outcomes:
            print("1" + outcome)
            await ctx.message.channel.send(
                "You need to format your message such as \n`.roulette [odd/even/zero] [amount of karma between 10 and 250]`")
            return
        try:
            amount = int("".join(amount))
        except ValueError:
            await ctx.message.channel.send(
                "You need to format your message such as \n`.roulette [odd/even/zero] [amount of karma 10 and 250]`")

        if 10 > amount or 250 < amount:
            await ctx.message.channel.send(
                "You need to format your message such as \n`.roulette [odd/even/zero] [amount of karma 10 and 250]`")
            return

        if amount > karma.get_karma(ctx.message.author.id):
            await ctx.message.channel.send(
                "You only have `{}` karma available for betting".format(karma.get_karma(ctx.message.author.id)))
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

    @client.command(aliases=["bannedword", "bannedwordlist"], description="Lists all banned words/terms", brief="Lists all banned words/terms")
    @commands.has_role(settings.verified_role_name)
    async def bannedwords(self, ctx):
        banned_words = settings.get_json("banned_words.json")
        lower = [item.lower() for item in banned_words]

        await ctx.message.channel.send("**Banned Words List:** \n• {}".format("\n• ".join(lower)))

    '''
    @client.command()
    @commands.has_role(settings.verified_role_name)
    async def jpeg(self, ctx, *args):
        pass
    '''

    @client.command(description="👏 Makes 👏 this 👏 text 👏 with 👏 any 👏 emote 👏", usage="[emote] [text]", brief="Replaces all spaces in [text] with 2 spaces and emote between them")
    @commands.has_role(settings.verified_role_name)
    async def generate(self, ctx, emote: str, *text):
        emote = emote
        text = " ".join(text)

        await ctx.send(str(text).replace(" ", " " + emote) + " " + emote)

    @client.command(description="Displays who has the highest karam/level", usage="[kind] (karma/level)", brief="Displays who has the highest [kind]")
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
            try:
                name = file[user]['name']
            except KeyError:
                name = await self.client.get_user_info(file[user])
                karma.set_name(name)

            try:
                value = file[user].get(type_new, 0)
            except KeyError:
                value = 0

            msg += '__{}__. **{}** {} `{}` {} \n'.format(
                number + 1, name, word, value, type_new)
        await ctx.send(msg)

    @client.command(description="Lists all invites to the server", brief="Lists all invites to the serve")
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
                              color=settings.embed_color)
        if unlimited_invites:
            embed.add_field(name='Unlimited Invites ({})'.format(len(unlimited_invites)),
                            value='\n'.join(unlimited_invites[:5]))
        if limited_invites:
            embed.add_field(name='Temporary/Finite Invites ({})'.format(len(limited_invites)),
                            value='\n'.join(limited_invites))
        if revoked_invites:
            embed.add_field(name='Revoked Invites ({})'.format(len(revoked_invites)), value='\n'.join(revoked_invites))
        await ctx.send(embed=embed)

    @client.command(aliases=["roast"], description="Insults a user", usage="[@user]", brief="Roasts [@user] with one of 180+ insults")
    @commands.has_role(settings.verified_role_name)
    async def insult(self, ctx, user: discord.Member):
        insults = settings.get_json("insults.json")

        if user == self.client.user:
            await ctx.message.channel.send(
                "How original. No one else had thought of trying to get the bot to insult itself. I applaud your "
                "creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any "
                "conversation. You are more of a bot than I, predictable answers, and absolutely dull to converse "
                "with.")
            return
        await ctx.message.channel.send("<@{}>, {}".format(user.id, random.choice(insults)))


def setup(client):
    client.add_cog(Verified(client))

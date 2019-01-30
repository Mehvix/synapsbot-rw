# coding=utf-8

import os
import sys
import json
import time
import asyncio
from datetime import datetime, timedelta

import karma
import curtime
import settings

import discord
from discord.ext import commands


class Admin:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client
        self.bannedusers = {}

    print("Loading Admin...")

    @client.event
    async def on_message_edit(self, before, after):
        banned_words = settings.get_json("banned_words.json")

        if any(word in str(after.content).upper() for word in banned_words):
            await before.author.send(
                "NO POOPY DOOPY WORDSIES!1! THE HECKIN BOOPIN POOPIN DOOPIN PUPPER SUPPER LUPPER DOGGO "
                "NIGGOS NOT LIEK IT!!! BRB HAVIN A ZOOMIE! XDDDLOLOELELALA \nYou can see what is banned "
                "via the `.bannedwords` command.")

            await after.delete()

    @client.event
    async def on_message(self, message):
        banned_words = settings.get_json("banned_words.json")

        if any(word in str(message.content).upper() for word in banned_words):
            await message.author.send(
                "NO POOPY DOOPY WORDSIES!1! THE HECKIN BOOPIN POOPIN DOOPIN PUPPER SUPPER LUPPER DOGGO "
                "NIGGOS NOT LIEK IT!!! BRB HAVIN A ZOOMIE! XDDDLOLOELELALA \nYou can see what is banned "
                "via the `.bannedwords` command.")

            await message.delete()

    @client.event
    async def on_member_update(self, before, after):
        # Banned Words
        banned_words = settings.get_json("banned_words.json")

        if any(word in str(after.nick).upper() for word in banned_words):
            await after.edit(nick=before.nick)

            await before.send("NO POOPY DOOPY WORDSIES!1! THE HECKIN BOOPIN POOPIN DOOPIN PUPPER SUPPER LUPPER DOGGO "
                              "NIGGOS NOT LIEK IT!!! BRB HAVIN A ZOOMIE! XDDDLOLOELELALA \nYou can see what is banned "
                              "via the `.bannedwords` command.")

    @client.command(aliases=['clear', 'snap'], description="Deletes messages", usage="(However man messages)", brief="Deletes messages")
    @commands.has_role(settings.admin_role_name)
    async def clean(self, ctx, messages: int):
        deleted = await ctx.channel.purge(limit=messages + 1)
        await ctx.send('`{}` deleted `{}` message(s)'.format(ctx.message.author.name, len(deleted) - 1))

    @client.command(aliases=["rules"], description="Displays Rules for the Server", brief="Used for the rules-and-info channel")
    @commands.has_role(settings.admin_role_name)
    async def serverrules(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Synaps Rules and Info",
                              url="https://steamcommunity.com/groups/team_synaps",
                              color=settings.embed_color)
        embed.set_thumbnail(url="https://goo.gl/ibJU2z")
        embed.add_field(name="📜 Rules 1.)", value="No spamming.", inline=True)
        embed.add_field(name="👙 Rules 2.)", value="No NSFW in Discussion.", inline=True)
        embed.add_field(name="🎵 Rules 3.)", value="No music requests in any channel but the music channel",
                        inline=True)
        embed.add_field(name="🔰 Getting Verified:",
                        value="Add `[Synaps]` to your steam name and DM a Admin.", inline=True)
        embed.add_field(
            name="🔸 Getting Member *(How to get access to other channels)*:",
            value="Read the rules above and type `.accept` in this channel. If you do not agree, type `.decline`",
            inline=True)
        await ctx.message.channel.send(embed=embed)

    @client.command(aliases=["gift"], description="Used to rewards users", usage="[@user] [amount]", brief="Used to reward members of the server")
    @commands.has_role(settings.admin_role_name)
    async def givekarma(self, ctx, target: discord.Member, amount: int):
        karma.user_add_karma(target.id, amount)
        await ctx.message.channel.send("You gave <@{}> `{}` karma. They now have a total of `{}` karma".format(
            target.id, amount, karma.get_karma(target.id)))

    @client.command(description="Mutes Target", usage="[@user]", brief="Prevents spam by adding @muted role to the user")
    @commands.has_role(settings.admin_role_name)
    async def mute(self, ctx, target: discord.Member):
        role = discord.utils.get(ctx.message.guild.roles, name=settings.mute_role_name)
        await target.add_roles(role)
        await ctx.send("<@{0}> muted <@{1}>".format(ctx.message.author.id, target.id))

    @client.command(description="Unmutes user", usage="[@user]", brief="Unmutes user")
    @commands.has_role(settings.admin_role_name)
    async def unmute(self, ctx, target: discord.Member):
        role = discord.utils.get(ctx.message.guild.roles, name=settings.mute_role_name)
        await target.remove_roles(role)
        await ctx.send("<@{0}> unmuted <@{1}>".format(ctx.message.author.id, target.id))

    @client.command(description="Adds [word] to the bannedword list", usage="[word]", brief="Adds [word] to a list that will prevent said word being in names or text channels. The list can be found via .bannedwords")
    @commands.has_role(settings.admin_role_name)
    async def banword(self, ctx, *word):
        word = " ".join(word)
        word = word.upper()
        fp = "banned_words.json"
        banned_words = settings.get_json(fp)
        banned_words.insert(0, word)
        with open(fp, 'w') as outfile:
            json.dump(banned_words, outfile)
        await ctx.send(
            "The word / sentence `{}` was banned. The full list of banned words can be found via `.bannedwords`".format(
                word))

    @client.command(description="Nicknames user", usage="[@user]", brief="Nicknames user")
    @commands.has_role(settings.admin_role_name)
    async def nick(self, ctx, nick_target: discord.Member, *nickname):
        nickname = " ".join(nickname)
        await ctx.send("Set `{}`'s nick to `{}`".format(nick_target.name, nickname))
        await nick_target.edit(nick=nickname)

    # Kick and Ban commands / events
    @client.command(description="Kicks user", usage="[@user(s)]", brief="Kicks user(s)")
    @commands.has_role(settings.admin_role_name)
    async def kick(self, ctx, targets: commands.Greedy[discord.Member], *reason: str):
        reason = " ".join(reason)
        for target in targets:
            if reason != "()":
                await target.kick(reason="{} ({}) used .kick command with the reason {}".format(ctx.message.author.name,
                                                                                                ctx.message.author.id,
                                                                                                reason))
            else:
                await target.kick(
                    reason="{} ({}) used .kick command".format(ctx.message.author.name, ctx.message.author.id))

    @client.command(description="Bans user", usage="[@user]", brief="Bans user(s)")
    @commands.has_role(settings.admin_role_name)
    async def ban(self, ctx, targets: commands.Greedy[discord.Member], *reason: str):
        reason = " ".join(reason)
        for target in targets:
            if reason != "()":
                await target.ban(reason="{} ({}) used .ban command with the reason {}".format(ctx.message.author.name,
                                                                                                ctx.message.author.id,
                                                                                                reason))
            else:
                await target.ban(
                    reason="{} ({}) used .ban command".format(ctx.message.author.name, ctx.message.author.id))

    @client.command(description="Bans user", usage="[@user]", brief="Bans user(s)")
    @commands.has_role(settings.admin_role_name)
    async def unban(self, ctx, targets: commands.Greedy[discord.Member], *reason: str):
        reason = " ".join(reason)
        for target in targets:
            if reason != "()":
                await target.unban(reason="{} ({}) used .unban command with the reason {}".format(ctx.message.author.name,
                                                                                                ctx.message.author.id,
                                                                                                reason))
            else:
                await target.unban(
                    reason="{} ({}) used .unban command".format(ctx.message.author.name, ctx.message.author.id))

    @client.event
    async def on_member_remove(self, member):
        guild = member.guild
        event = await guild.audit_logs(limit=1).flatten()

        print(event)
        print(event == discord.AuditLogAction.kick)

        user_was_kicked = False
        reason = ""
        kicker = ""
        event = event[0]

        if event.target == member:
            user_was_kicked = True
            reason = event.reason
            kicker = event.user

        # Wait for the ban event to fire (if at all)
        await asyncio.sleep(0.25)
        if member.guild.id in self.bannedusers and \
                member.id == self.bannedusers[member.guild.id]:
            del self.bannedusers[member.guild.id]
            return

        member_created_at_date = str(member.created_at).split('.', 1)[0]
        avatar = member.avatar_url if member.avatar else member.default_avatar_url

        embed = discord.Embed(color=settings.embed_color)
        if user_was_kicked is True:
            embed.add_field(name="Kicker:", value=kicker, inline=False)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.set_author(name="{} was kicked from the server 👋".format(member.name))  # todo replace this with boot emoji once it comes out
        else:
            embed.set_author(name="{} left the server 🙁".format(member.name))
        embed.add_field(name="Username:", value="{}#{}".format(member.name, member.discriminator), inline=False)
        embed.add_field(name="Time Left:", value=curtime.get_time(), inline=False)
        embed.add_field(name="Account Created at:", value=member_created_at_date, inline=False)
        embed.add_field(name="User Avatar URL:", value=member.avatar_url)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="We now have {} members".format(member.guild.member_count))
        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send(embed=embed)

    @client.command(description="DM's a user", usage="[text]", brief="DM's user [text]")
    @commands.has_role(settings.admin_role_name)
    async def dm(self, user: discord.Member, msg: str):
        await user.send(msg)

    @client.event
    async def on_member_ban(self, guild, member):
        self.bannedusers[guild.id] = member.id

        event = await guild.audit_logs(action=discord.AuditLogAction.ban).flatten()
        event = event[0]
        reason = event.reason

        member_created_at_date = str(member.created_at).split('.', 1)[0]
        avatar = member.avatar_url if member.avatar else member.default_avatar_url

        embed = discord.Embed(color=settings.embed_color)
        embed.set_author(name="{} was banned from the server 🔨".format(member.name))
        embed.add_field(name="Username:", value="{}#{}".format(member.name, member.discriminator), inline=False)
        embed.add_field(name="Time Banned:", value=curtime.get_time(), inline=False)
        embed.add_field(name="Account Created at:", value=member_created_at_date, inline=False)
        embed.add_field(name="Banner:", value="{}#{}".format(event.user.name, event.user.discriminator), inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Ban ID:", value=event.id, inline=False)
        embed.add_field(name="User Avatar URL:", value=member.avatar_url)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="We now have {} members".format(member.guild.member_count))

        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send(embed=embed)

    @client.event
    async def on_member_unban(self, guild, member):
        channel = self.client.get_channel(id=settings.notification_channel)
        await channel.send('{} (`{}`) was unbanned from the server :unlock:'.format(member.mention, member))

    # Cog Commands
    # todo: add disable commands here

    @client.command(description="Loads a cog", usage="[cog name]", brief="Loads [cog name]")
    @commands.has_role(settings.admin_role_name)
    async def load(self, extension_name: str):
        try:
            client.load_extension(extension_name)
            print("LOADED {}".format(extension_name))
        except (AttributeError, ImportError) as error:
            await print("```py\n{}: {}\n```".format(type(error).__name__, str(error)))
            return
        print("{} loaded.".format(extension_name))

    @client.command(description="Unloads a cog", usage="[cog name]", brief="Unloads [cog name]")
    @commands.has_role(settings.admin_role_name)
    async def unload(self, extension_name: str):
        client.unload_extension(extension_name)
        print("{} unloaded.".format(extension_name))


def setup(client):
    client.add_cog(Admin(client))

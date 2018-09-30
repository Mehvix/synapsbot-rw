# coding=utf-8

import os
import sys
import json
import time
import karma
import curtime
import discord
import settings
from discord.ext import commands
from datetime import datetime, timedelta


class Admin:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

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

    @client.command(aliases=['clear'], description="Deletes messages", usage="(However man messages)", brief="Deletes messages")
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

    @client.command(description="Bans user", usage="[@user]", brief="Bans user")
    @commands.has_role(settings.admin_role_name)
    async def ban(self, ctx, target: discord.Member):
        await target.ban()
        await ctx.message.channel.send("{} banned <@{}>".format(ctx.message.author.name, target.id))

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

    @client.command(description="Kicks user", usage="[@user]", brief="Kicks user")
    @commands.has_role(settings.admin_role_name)
    async def kick(self, ctx, kick_target: discord.Member):
        await kick_target.kick(reason="{} ({}) used .kick command".format(ctx.message.author.name, ctx.message.author.id))
        await ctx.send("{} kicked <@{}>".format(ctx.message.author.name, kick_target.id))

    @client.command(description="Nicknames user", usage="[@user]", brief="Nicknames user")
    @commands.has_role(settings.admin_role_name)
    async def nick(self, ctx, nick_target: discord.Member, *nickname):
        nickname = " ".join(nickname)
        await ctx.send("Set `{}`'s nick to `{}`".format(nick_target.name, nickname))
        await nick_target.edit(nick=nickname)

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

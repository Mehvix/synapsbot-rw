#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json

import discord

import settings

red = ":red:481329772102942740"
orange = ":orange:481329772232704010"
yellow = ":yellow:481329771754553345"
green = ":green:481329615491563520"
blue = ":blue:481329615483437057"
indigo = ":indigo:481329772153012225"
violet = ":violet:481329771809210369"
white = ":white:481329771700289538"
black = ":black:484770699790254091"


class Canvas:
    def __init__(self, client):
        self.client = client

    print("Loading Canvas...")

    async def send_canvas(self):
        with open('canvas.json') as fp:
            file_content = json.load(fp)
        global a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

        channel = self.client.get_channel(settings.canvas_channel)

        a = await channel.send("{}".format(" ".join(file_content['a'])))
        b = await channel.send("{}".format(" ".join(file_content['b'])))
        c = await channel.send("{}".format(" ".join(file_content['c'])))
        d = await channel.send("{}".format(" ".join(file_content['d'])))
        e = await channel.send("{}".format(" ".join(file_content['e'])))
        f = await channel.send("{}".format(" ".join(file_content['f'])))
        g = await channel.send("{}".format(" ".join(file_content['g'])))
        h = await channel.send("{}".format(" ".join(file_content['h'])))
        i = await channel.send("{}".format(" ".join(file_content['i'])))
        j = await channel.send("{}".format(" ".join(file_content['j'])))
        k = await channel.send("{}".format(" ".join(file_content['k'])))
        l = await channel.send("{}".format(" ".join(file_content['l'])))
        m = await channel.send("{}".format(" ".join(file_content['m'])))
        n = await channel.send("{}".format(" ".join(file_content['n'])))
        o = await channel.send("{}".format(" ".join(file_content['o'])))
        p = await channel.send("{}".format(" ".join(file_content['p'])))
        q = await channel.send("{}".format(" ".join(file_content['q'])))
        r = await channel.send("{}".format(" ".join(file_content['r'])))
        s = await channel.send("{}".format(" ".join(file_content['s'])))
        t = await channel.send("{}".format(" ".join(file_content['t'])))
        u = await channel.send("{}".format(" ".join(file_content['u'])))
        v = await channel.send("{}".format(" ".join(file_content['v'])))
        w = await channel.send("{}".format(" ".join(file_content['w'])))
        x = await channel.send("{}".format(" ".join(file_content['x'])))
        y = await channel.send("{}".format(" ".join(file_content['y'])))
        z = await channel.send("{}".format(" ".join(file_content['z'])))
        await channel.send(":black_large_square: :black_large_square: :black_large_square: :black_large_square: "
                           ":black_large_square: :black_large_square: :black_large_square: :black_large_square: "
                           ":black_large_square: :black_large_square: :black_large_square: :one: :one: :one: :one: "
                           ":one: :one: :one: :one: :one: :one: :two: :two: :two: :two: :two: :two:")
        await channel.send(":black_large_square: :zero: :one: :two: :three: :four: :five: :six: :seven: :eight: "
                           ":nine: :zero: :one: :two: :three: :four: :five: :six: :seven: :eight: :nine: :zero: :one: "
                           ":two: :three: :four: :five:")
        await channel.send("**Colors:**\n<{}> = Red\n<{}> = Orange\n<{}> = Yellow\n<{}> = Green\n<{}> = Blue\n<{}> = "
                           "Indigo\n<{}> = Violet\n<{}> = White\n<{}> = Black".format(red, orange, yellow, green,
                                                                                      blue, indigo, violet, white,
                                                                                      black))
        return

    async def on_ready(self):
        channel = self.client.get_channel(settings.canvas_channel)
        messages = []

        try:
            async for message in channel.history(limit=32):
                messages.append(message)
            await channel.delete_messages(messages)
        except discord.ClientException:
            pass  # channel has no messages

        embed = discord.Embed(color=settings.embed_color)
        embed.add_field(name="Client was (re)started", value="Updating Canvas..")
        await channel.send(embed=embed)
        await self.send_canvas()

    async def on_message(self, message):
        global emoji_color, line_content
        user_id = message.author.id

        if message.channel.id == settings.canvas_channel:
            if message.content.upper() == ".DRAW SAVED":
                if message.author.server_permissions.administrator:
                    await message.delete()
                    await self.send_canvas()
                    return

            else:
                if user_id == self.client.user.id:
                    return

                args = str(message.content).split(" ")

                try:
                    pos = args[0]
                    color = args[1]

                    posy = pos[0]  # A
                    posx = int(pos[1:]) + 1  # 4
                except IndexError:
                    await message.author.send("Your message was incorrectly formatted! It should look like `a3 red` or `g0 blue`")
                    await message.delete()
                    return

                print("COLOR:" + color)
                print("POSX: {}".format(posx))
                print("POSY: {}".format(posy))

                if color.lower() == "red":
                    emoji_color = red
                if color.lower() == "white":
                    emoji_color = white
                if color.lower() == "orange":
                    emoji_color = orange
                if color.lower() == "yellow":
                    emoji_color = yellow
                if color.lower() == "green":
                    emoji_color = green
                if color.lower() == "blue":
                    emoji_color = blue
                if color.lower() == "indigo":
                    emoji_color = indigo
                if color.lower() == "violet":
                    emoji_color = violet
                if color.lower() == "black":
                    emoji_color = black
                if emoji_color is None:
                    await message.author.send(
                        "Your message was incorrectly formatted! It should look like `a3 red` or `g0 blue`")
                    await message.delete()
                    return

                with open('canvas.json') as fp:
                    content = json.load(fp)

                try:
                    if posy.lower() == "a":
                        line_content = content['a']
                        line = a
                    if posy.lower() == "b":
                        line_content = content['b']
                        line = b
                    if posy.lower() == "c":
                        line_content = content['c']
                        line = c
                    if posy.lower() == "d":
                        line_content = content['d']
                        line = d
                    if posy.lower() == "e":
                        line_content = content['e']
                        line = e
                    if posy.lower() == "f":
                        line_content = content['f']
                        line = f
                    if posy.lower() == "g":
                        line_content = content['g']
                        line = g
                    if posy.lower() == "h":
                        line_content = content['h']
                        line = h
                    if posy.lower() == "i":
                        line_content = content['i']
                        line = i
                    if posy.lower() == "j":
                        line_content = content['j']
                        line = j
                    if posy.lower() == "k":
                        line_content = content['k']
                        line = k
                    if posy.lower() == "l":
                        line_content = content['l']
                        line = l
                    if posy.lower() == "m":
                        line_content = content['m']
                        line = m
                    if posy.lower() == "n":
                        line_content = content['n']
                        line = n
                    if posy.lower() == "o":
                        line_content = content['o']
                        line = o
                    if posy.lower() == "p":
                        line_content = content['p']
                        line = p
                    if posy.lower() == "q":
                        line_content = content['q']
                        line = q
                    if posy.lower() == "r":
                        line_content = content['r']
                        line = r
                    if posy.lower() == "s":
                        line_content = content['s']
                        line = s
                    if posy.lower() == "t":
                        line_content = content['t']
                        line = t
                    if posy.lower() == "u":
                        line_content = content['u']
                        line = u
                    if posy.lower() == "v":
                        line_content = content['v']
                        line = v
                    if posy.lower() == "w":
                        line_content = content['w']
                        line = w
                    if posy.lower() == "x":
                        line_content = content['x']
                        line = x
                    if posy.lower() == "y":
                        line_content = content['y']
                        line = y
                    if posy.lower() == "z":
                        line_content = content['z']
                        line = z

                except (TypeError, NameError) as error:
                    messages = []
                    async for message in self.client.logs_from(message.channel, limit=30):
                        messages.append(message)
                    await self.client.delete_messages(messages)

                    await self.client.send_message(message.channel, "ERROR: `{}`\nReloading Canvas...".format(error))

                    embed = discord.Embed(title="Canvas Help:", color=settings.embed_color)
                    embed.add_field(name="[LETTER][NUMBER] [COLOR]",
                                    value="Paints tile in row [letter] and line [number] to color [color]",
                                    inline=False)
                    embed.add_field(name="Example:", value="a3 red", inline=False)
                    embed.set_footer(text="You can also try `.help verified`, `.help admin`, & `.help basic`")
                    await self.client.send_message(message.channel, embed=embed)

                    await send_canvas(settings.canvas_channel)
                    return

                if not line_content:
                    if message.guild.owner.id != user_id:
                        await message.author.send(
                            "Your message was incorrectly formatted! It should look like `a3 red` or `g0 blue`")
                        await message.delete()
                        return

                    else:
                        await message.delete()

                old_content = line_content
                print("Old content: {}".format(old_content))

                place = int(posx)
                print("Place: {}".format(place))

                emote = str(emoji_color)
                print("Emote: " + emote)

                new_content = list(old_content)
                del new_content[int(posx)]
                new_content.insert(int(posx), "<{}>".format(str(emoji_color)))
                print("New content: {}".format(new_content))

                print("line: {}".format(line))
                await line.edit(content=" ".join(new_content))

                with open('canvas.json', 'r') as fp:
                    content = json.load(fp)
                content[posy.lower()] = new_content
                with open('canvas.json', 'w') as fp:
                    json.dump(content, fp, sort_keys=True, indent=4)

            if message.author.id != self.client.user.id:
                await asyncio.sleep(1)
                await message.delete()


def setup(client):
    client.add_cog(Canvas(client))

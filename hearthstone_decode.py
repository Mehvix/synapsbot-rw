#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import hashlib
import aiohttp
import asyncio
import hearthstone

from bs4 import BeautifulSoup
from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType

import settings

import discord
from discord.ext import commands


class decode(commands.Cog):
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading Decoder...")

    @commands.command(aliases=["hs", "decode"], usage="[deckstring]", description="Decodes HS deckstring", brief="Decode [deckstring]")
    async def deck(self, ctx, target: str):
        deck = Deck.from_deckstring(target)

        image = ""
        hero = deck.heroes[0]
        if str(hero) == "274" or str(hero) == "50484":
            hero = "Druid"
            image ="https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/8/8d/Icon_Druid_64.png?version=b6a84e24ff9417d99c04f883b5687ed3"
        if str(hero) == "637" or str(hero) == "2829" or str(hero) == "39117":
            hero = "Mage"
            image ="https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/f/f2/Icon_Mage_64.png?version=f16b540384ed113585c2f6b117aeb7d0"
        if str(hero) == "31" or str(hero) == "2826":
            hero = "Hunter"
            image ="https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/f/f4/Icon_Hunter_64.png?version=b9ee98cd8936a875ba84bc9d3f83bebc"
        if str(hero) == "7" or str(hero) == "2828":
            hero = "Warrior"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/1/19/Icon_Warrior_64.png?version=d0252ccedf6faab67e5ab506dddda2ea"
        if str(hero) == "893" or str(hero) == "47817" or str(hero) == "51834":
            hero = "Warlock"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/2/2e/Icon_Warlock_64.png?version=5f7037f5cb0b4be064ceb9f6c4528e73"
        if str(hero) == "1066" or str(hero) == "40183":
            hero = "Shaman"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/a/a8/Icon_Shaman_64.png?version=08bc485fb8261048c7a3a480953c7169"
        if str(hero) == "930":
            hero = "Rogue" or str(hero) == "40195"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/7/76/Icon_Rogue_64.png?version=04949ddceba669263317bf44edb981c1"
        if str(hero) == "813"  or str(hero) == "41887":
            hero = "Priest"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/2/23/Icon_Priest_64.png?version=a5d7b4e15c40dfd667e6868165b10677"
        if str(hero) == "671" or str(hero) == "2827" or str(hero) == "46116":
            hero = "Paladin"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/7/7b/Icon_Paladin_64.png?version=2a4e7cdbb3b5402f3e8a34ea156f9cf1"

        embed = discord.Embed()
        num_of_spells = 0
        num_of_minions = 0

        deckids = []
        fulldeck = []
        total_cost = 0
        for card in deck.cards:
            num_of_cards = card[1]
            card = card[0]
            search = "https://api.hearthstonejson.com/v1/26996/enUS/cards.collectible.json"
            async with aiohttp.ClientSession() as session:
                async with session.get(search) as r:
                    result = await r.json(content_type='application/json')

                    x = 0
                    while x < len(result):
                        z = result[x]["dbfId"]
                        if z == card:
                            # todo: add expansion, hsreplay link/data, etc.

                            for _ in range(num_of_cards):
                                deckids.append(str(result[x]["id"]))

                            types_of_rarity = ["🏛️", "💿", "💙", "💜", "💛"]  # free, common, rare, epic, legendary

                            name = result[x]["name"]
                            cost = result[x]["cost"]
                            rarity = result[x]["rarity"]

                            if result[x]["type"] == "SPELL":
                                num_of_spells += (1 * num_of_cards)

                            if result[x]["type"] == "MINION":
                                num_of_minions += (1 * num_of_cards)

                            if rarity == "LEGENDARY":
                                total_cost += 1600 * int(num_of_cards)
                                rarity = types_of_rarity[4]
                            if rarity == "EPIC":
                                total_cost += 400 * int(num_of_cards)
                                rarity = types_of_rarity[3]
                            if rarity == "RARE":
                                total_cost += 100 * int(num_of_cards)
                                rarity = types_of_rarity[2]
                            if rarity == "COMMON":
                                total_cost += 40 * int(num_of_cards)
                                rarity = types_of_rarity[1]
                            if rarity == "FREE":
                                rarity = types_of_rarity[0]

                            y = [str(num_of_cards), " x ", str(rarity) + " | ", str(name), "| " + str(cost) + " mana |", int(cost)]
                            fulldeck.append(y)
                            x = len(result)
                        else:
                            x += 1

        def getcost(elem):
            return elem[-1]

        fulldeck.sort(key=getcost, reverse=True)

        ALPHABET = string.ascii_letters + string.digits

        # The following is yoinked from here:
        # https://github.com/HearthSim/HSReplay.net/blob/54a5e372e6ddd870fa102c7e827c359c28b81187/scripts/generating_deck_ids_example.py
        def int_to_string(number, alphabet, padding=None):
            """
            Convert a number to a string, using the given alphabet.
            """
            output = ""
            alpha_len = len(alphabet)
            while number:
                number, digit = divmod(number, alpha_len)
                output += alphabet[digit]
            if padding:
                remainder = max(padding - len(output), 0)
                output = output + alphabet[0] * remainder
            return output

        def generate_digest_from_deck_list(id_list):
            sorted_cards = sorted(id_list)
            m = hashlib.md5()
            m.update(",".join(sorted_cards).encode("utf-8"))
            return m.hexdigest()

        card_ids = deckids
        digest = generate_digest_from_deck_list(card_ids)
        shortid = int_to_string(int(digest, 16), ALPHABET)

        embed = discord.Embed(title="{}'s Deck".format(ctx.author.name),
                              description="• Deckcode being used:\n`{}`"
                                          "\n[• View deck stats on HSReplay](https://hsreplay.net/decks/{}/)"
                              .format(deck.as_deckstring, shortid),
                              color=settings.embed_color)
        embed.add_field(name="Format:", value=str(str(deck.format)[14:]).title(), inline=False)
        embed.add_field(name="Cost:", value=str(total_cost), inline=False)
        if num_of_spells < num_of_minions:
            embed.add_field(name="Minions to Spells Ratio:",
                            value="{} : 1".format(str(num_of_minions / num_of_spells)[:5]), inline=False)
        else:
            embed.add_field(name="Minions to Spell Ratio:",
                            value="{} : 1".format(str(num_of_spells / num_of_minions)[:5]), inline=False)
        embed.set_thumbnail(url=image)
        embed.add_field(name="# of Spells:", value=str(num_of_spells), inline=False)
        embed.add_field(name="# of Minions:", value=str(num_of_minions), inline=False)
        embed.add_field(name="Cards:", value='\n'.join(' '.join(elems[:-1]) for elems in fulldeck), inline=False)
        await asyncio.sleep(1)
        await ctx.send(embed=embed)

        search = "https://hsreplay.net/decks/{}/#tab=overview".format(shortid)
        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                text = await r.read()
                await asyncio.sleep(1)
                soup = BeautifulSoup(text.decode('utf-8'), 'html5lib')
                data = soup.find('span', attrs={'class': 'infobox-value'})


def setup(client):
    client.add_cog(decode(client))

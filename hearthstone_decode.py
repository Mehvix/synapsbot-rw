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

    @commands.command(aliases=["hs", "decode"], usage="[deckstring]", description="Decodes HS deckstring",
                      brief="Decode [deckstring]")
    async def deck(self, ctx, target: str):
        deck = Deck.from_deckstring(target)

        image = ""
        hs_class = deck.heroes[0]

        # You can get hero ID's via https://www.hearthstonedb.net/cards/heroes-set
        # todo automate this process^
        if str(hs_class) == "274" or "50484":
            hs_class = "Druid"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/1/13/Icon_Druid_48.png?version=04fe2182b995ef2bfa95a2782410a212"
        elif str(hs_class) == "637" or "2829" or "39117":
            hs_class = "Mage"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/a/ad/Icon_Mage_48.png?version=490a29a8d96557bb64f6b7bd825713cc"
        elif str(hs_class) == "31" or "2826":
            hs_class = "Hunter"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/8/82/Icon_Hunter_48.png?version=ad01d4f022ef5af731a6b9c41be9df58"
        elif str(hs_class) == "7" or "2828":
            hs_class = "Warrior"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/e/e8/Icon_Warrior_48.png?version=3fcf2ff09c6334756e9005ac69b77949"
        elif str(hs_class) == "893" or "47817" or "51834":
            hs_class = "Warlock"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/c/c3/Icon_Warlock_48.png?version=15d8a6846eff7ebd47fc439a7b3b0719"
        elif str(hs_class) == "1066" or "40183" or "53237":
            hs_class = "Shaman"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/d/da/Icon_Shaman_48.png?version=825a713ad65dcbd374e3501edc8fb42b"
        elif str(hs_class) == "930" or "40195":
            hs_class = "Rogue"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/1/13/Icon_Rogue_48.png?version=cc4b41c03ccdb9b0f666839ed1f72a51"
        elif str(hs_class) == "813" or "41887" or "54816":
            hs_class = "Priest"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/3/30/Icon_Priest_48.png?version=dc21614bcf47a51b6a28110fa639150e"
        elif str(hs_class) == "671" or "2827" or "46116" or "53187":
            hs_class = "Paladin"
            image = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/d/d3/Icon_Paladin_48.png?version=3386c8ba02bde1df93154aa6f595aa0e"

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

                            y = [str(num_of_cards), " x ", str(rarity) + " | ", str(name), "| " + str(cost) + " mana |",
                                 int(cost)]
                            fulldeck.append(y)
                            x = len(result)
                        else:
                            x += 1

        def getcost(elem):
            return elem[-1]

        fulldeck.sort(key=getcost, reverse=True)

        alphabet = string.ascii_letters + string.digits

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
        shortid = int_to_string(int(digest, 16), alphabet)

        embed = discord.Embed(title="{}'s Deck".format(ctx.author.name),
                              description="• Deckcode being used:\n`{}`"
                                          "\n[• View deck stats on HSReplay](https://hsreplay.net/decks/{}/)"
                              .format(deck.as_deckstring, shortid),
                              color=settings.embed_color)
        embed.add_field(name="Format:", value=str(str(deck.format)[14:]).title(), inline=False)
        embed.add_field(name="Class:", value=hs_class.title(), inline=False)
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
                # ^hmmm idk what I was gonnna do with this, but I'll leave it in incase I come back around to this


def setup(client):
    client.add_cog(decode(client))

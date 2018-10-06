#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp
import asyncio

import hearthstone
from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType

import settings

import discord
from discord.ext import commands


class decode:
    client = commands.Bot(command_prefix='.')

    def __init__(self, client):
        self.client = client

    print("Loading decode...")

    @commands.command(aliases=["hs", "decode"], usage="[deckstring]", description="Decodes HS deckstring", brief="Decode [deckstring]")
    async def deck(self, ctx, target: str):
        deck = ""
        if target == "druid":
            deck = Deck.from_deckstring("AAECAZICApnTAvX8Ag5AX/0C5gXkCJvLAqDNAofOAo7QApjSAp7SAtvTAtfvAuL4AgA=")
        if target == "hunter":
            deck = Deck.from_deckstring("AAECAR8I+AjtCdPFAobTApziArbqAsvsAoDzAguNAZcIq8IC2MICnM0C3dICi+EC4eMC8vECufgC4vgCAA==")
        if target == "mage":
            deck = Deck.from_deckstring("AAECAf0EBHHtBaLTAu72Ag27ApUDqwS0BOYElgXsBcHBApjEAo/TAvvsApX/Arn/AgA=")
        if target == "pali":
            deck = Deck.from_deckstring("AAECAZ8FBK8EpwXxBZ74Ag1G9QX5CpvCAuvCAoPHArjHAuPLApXOAvvTAtHhAtblArXmAgA=")
        if target == "priest":
            deck = Deck.from_deckstring("AAECAa0GCgm0A+0F0wrXCr7IAubMAsLOAqCAA42CAwqXAqEE0cEC2MEC5cwCtM4C8M8C6NAC4+kCn+sCAA==")
        if target == "rogue":
            deck = Deck.from_deckstring("AAECAaIHBK8E/eoCnvgC5/oCDYwCywPUBfMF9QXdCIHCAp/CAuvCAtHhAovlAqbvAuL4AgA=")
        if target == "shaman":
            deck = Deck.from_deckstring("AAECAaoICP8F08UCnOICq+cCw+oCp+4C7/cCmfsCC4EE9QTeBf4Fsgb7DJfBAsfBApvLAvPnAu/xAgA=")
        if target == "warlock":
            deck = Deck.from_deckstring("AAECAf0GApziAo+CAw4whAH3BM4Hwgj3DJvLAp/OAvLQAtHhAofoAu/xAvT3AtP4AgA=")
        if target == "warrior":
            deck = Deck.from_deckstring("AAECAQcG+QzTxQLPxwKS+AKe+AKggAMMS6ICogTeBf8Hm8ICoscCyucC4vgCg/sCjvsCnvsCAA==")

        image = ""
        hero = deck.heroes[0]
        if str(hero) == "274":
            hero = "Druid"
            image ="https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/8/8d/Icon_Druid_64.png?version=b6a84e24ff9417d99c04f883b5687ed3"
        if str(hero) == "637":
            hero = "Mage"
            image ="https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/f/f2/Icon_Mage_64.png?version=f16b540384ed113585c2f6b117aeb7d0"
        if str(hero) == "31":
            hero = "Hunter"
            image ="https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/f/f4/Icon_Hunter_64.png?version=b9ee98cd8936a875ba84bc9d3f83bebc"
        if str(hero) == "7":
            hero = "Warrior"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/1/19/Icon_Warrior_64.png?version=d0252ccedf6faab67e5ab506dddda2ea"
        if str(hero) == "893":
            hero = "Warlock"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/2/2e/Icon_Warlock_64.png?version=5f7037f5cb0b4be064ceb9f6c4528e73"
        if str(hero) == "1066":
            hero = "Shaman"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/a/a8/Icon_Shaman_64.png?version=08bc485fb8261048c7a3a480953c7169"
        if str(hero) == "930":
            hero = "Rogue"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/7/76/Icon_Rogue_64.png?version=04949ddceba669263317bf44edb981c1"
        if str(hero) == "813":
            hero = "Priest"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/2/23/Icon_Priest_64.png?version=a5d7b4e15c40dfd667e6868165b10677"
        if str(hero) == "671":
            hero = "Paladin"
            image = "https://d1u5p3l4wpay3k.cloudfront.net/hearthstone_gamepedia/7/7b/Icon_Paladin_64.png?version=2a4e7cdbb3b5402f3e8a34ea156f9cf1"

        print(deck.cards)

        embed = discord.Embed(title="{}'s Deck 🃏".format(ctx.author.name),
                              description="Deckcode being used:\n`{}`".format(deck.as_deckstring),
                              color=settings.embed_color)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Format:", value=str(str(deck.format)[14:]).title(), inline=True)
        embed.add_field(name="Class:", value=hero, inline=True)

        fulldeck = []
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
                            # todo: add rarity, total cost, hsreplay link/data, etc.
                            types_of_rarity = ["🏛️", "💿", "💙", "💜", "💛"]  # free, common, rare, epic, legendary
                            total_cost = 0

                            name = result[x]["name"]
                            cost = result[x]["cost"]
                            rarity = result[x]["rarity"]

                            if rarity == "LEGENDARY":
                                rarity = types_of_rarity[4]
                            if rarity == "EPIC":
                                rarity = types_of_rarity[3]
                            if rarity == "RARE":
                                rarity = types_of_rarity[2]
                            if rarity == "COMMON":
                                rarity = types_of_rarity[1]
                            if rarity == "FREE":
                                rarity = types_of_rarity[0]

                            y = [str(num_of_cards), " x ", str(rarity) + " | ", str(name), "| " + str(cost) + " mana |", int(cost)]
                            fulldeck.append(y)
                            x = len(result)
                        else:
                            x += 1

        print("=============================================")

        def getcost(elem):
            return elem[-1]

        fulldeck.sort(key=getcost, reverse=True)

        embed.add_field(name="Cards:", value='\n'.join(' '.join(elems[:-1]) for elems in fulldeck), inline=True)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(decode(client))

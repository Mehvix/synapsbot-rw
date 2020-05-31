#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import subprocess
import sys


def random_clock():
    return random.choice(["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"])


def get_json(file_path):
    with open(file_path, 'r') as fp:
        return json.load(fp)


def get_version():
    try:
        args = ['git', 'describe', '--tags', '--always']
        return subprocess.check_output(args).decode('utf-8', 'ignore').strip()
    except subprocess.CalledProcessError as error:
        return f"Error: {error}"


def set_server(server):
    global token, embed_color, server_id
    global upvote_emoji, downvote_emoji
    global notification_channel, accept_channel, canvas_channel, pokemon_channel, game_channel, mc_data_channel
    global member_role_name, admin_role_name, verified_role_id, \
        verified_role_name
    global level_role, roles_role, groups_role, games_role, restriction_role
    global league_role, hs_role, fortnite_role, pubg_role, tf2_role, gta_role, \
        chiv_role, cs_role, aoe_role, civ_role, rainbow_role, brawl_role, ratz_role, \
        path_role, skribble_role, gmod_role, apex_role, mc_role, ll_blaze
    global snowboard_role, code_role, poker_role
    global lobby_one_vc_id, lobby_two_vc_id, lobby_one_role_id, lobby_two_role_id, hidden_chat_id, main_cat_id, \
        lobby_one_text_id, lobby_two_text_id
    global groups_message_id, games_message_id, games_channel_id

    embed_color = 0x593595

    global game_roles
    global group_roles

    if server == "test":
        print("Using TEST account")
        jsontoken = get_json('tokens.json')
        token = jsontoken.get("test")

        upvote_emoji = ":upvote:414204250642579488"
        downvote_emoji = ":downvote:414204250948894721"

        notification_channel = 414197286596247556

        member_role_name = "Member 🔸"
        admin_role_name = "Admin 💠"
        verified_role_name = "Verified 🔰"

        verified_role_id = 439191092991229992
        pokemon_channel = 439198154324181002

        accept_channel = 414974032048553984
        canvas_channel = 486702610745917460

    elif server == "main":
        print("Using MAIN account")
        jsontoken = get_json('tokens.json')
        token = jsontoken.get("main")

        upvote_emoji = ":upvote:412119803034075157"
        downvote_emoji = ":downvote:412119802904313858"

        notification_channel = 412075980094570506

        member_role_name = "Member 🔸"

        admin_role_name = "Admin 💠"

        verified_role_name = "Verified 🔰"
        verified_role_id = 366739104203014145

        pokemon_channel = 439198154324181002
        accept_channel = 356456207185215491
        canvas_channel = 482084251702132746

        # Notation Roles
        level_role = 490738787140370472
        roles_role = 490738558882021376
        groups_role = 490739316037910539
        games_role = 479745379399630858
        restriction_role = 490739413467398184

        # Game Roles (games.py)
        games_message_id = 490768003080650755
        game_channel = 490741754262192129
        league_role = 346535079390085120
        hs_role = 434513786972405761
        fortnite_role = 373673740304777216
        pubg_role = 346535016001699851
        tf2_role = 371431977234202624
        gta_role = 378718118152896512
        chiv_role = 346536597640183808
        cs_role = 368195375502327811
        aoe_role = 346535115393990656
        civ_role = 401585649872011274
        rainbow_role = 421846788534697984
        brawl_role = 488201787468414976
        ratz_role = 491388165618270218
        skribble_role = 495794541262143488
        gmod_role = 498645082745077770
        apex_role = 549115001302941727
        mc_role = 554822553885999110
        ll_blaze = 513838239031754763

        # Group Roles (games.py)
        groups_message_id = 495070906906050560
        code_role = 494998056794849290
        path_role = 491707496767946753
        poker_role = 442837936552017930
        snowboard_role = 378342844282306581

        games_channel_id = 490741754262192129

        # lobbytext.py
        lobby_one_vc_id = 358766565941837829
        lobby_two_vc_id = 441444115444400139

        lobby_one_role_id = 497234318830338049
        lobby_two_role_id = 497234329215434765

        hidden_chat_id = 497894067561299983
        main_cat_id = 412360523959631873

        lobby_one_text_id = 497235184693805056
        lobby_two_text_id = 497235830234939394

        mc_data_channel = 557049387310645248

        server_id = 236258442233380874

        group_roles = [code_role, poker_role, snowboard_role]
        game_roles = [league_role, hs_role, fortnite_role, pubg_role, tf2_role, gta_role, chiv_role, cs_role, aoe_role,
                      civ_role, rainbow_role, brawl_role, ratz_role, skribble_role, gmod_role, apex_role, mc_role,
                      ll_blaze]

        return
    else:
        sys.exit("No Server (main/test)")

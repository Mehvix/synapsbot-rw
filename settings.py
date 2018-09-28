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
    global token, upvote_emoji, downvote_emoji, notification_channel, member_role_id, member_role_name, shut_up_role, \
        admin_role_name, verified_role_id, admin_role_id, verified_role_name, pokemon_channel, mute_role_id, \
        mute_role_name, embed_color, accept_channel, canvas_channel, level_role, roles_role, groups_role, games_role, \
        restriction_role, game_channel, league_role, hs_role, fortnite_role, pubg_role, tf2_role, gta_role, \
        chiv_role, cs_role, aoe_role, civ_role, rainbow_role, brawl_role, ratz_role, code_role, boof_role, max_role, \
        path_role, poker_role, dj_role, snowboard_role, groups_message_id, games_message_id
    embed_color = 0x593595

    if server == "test":
        print("Using TEST account")
        jsontoken = get_json('tokens.json')
        token = jsontoken.get("test")

        upvote_emoji = ":upvote:414204250642579488"
        downvote_emoji = ":downvote:414204250948894721"

        notification_channel = 414197286596247556

        member_role_name = "Member 🔸"
        member_role_id = 414683704737267712
        admin_role_name = "Admin 💠"
        shut_up_role = 414237651504332800
        verified_role_name = "Verified 🔰"
        admin_role_id = 439175903600181269

        verified_role_id = 439191092991229992
        pokemon_channel = 439198154324181002

        mute_role_name = "Text Muted"
        mute_role_id = 445059188973109259

        accept_channel = 414974032048553984
        canvas_channel = 486702610745917460

        games_message_id = None
        groups_message_id = None
        level_role = None
        roles_role = None
        groups_role = None
        games_role = None
        restriction_role = None
        ratz_role = None
        return

    if server == "main":
        print("Using MAIN account")
        jsontoken = get_json('tokens.json')
        token = jsontoken.get("main")

        upvote_emoji = ":upvote:412119803034075157"
        downvote_emoji = ":downvote:412119802904313858"

        notification_channel = 412075980094570506

        member_role_name = "Member 🔸"
        member_role_id = 312693233329373194

        admin_role_name = "Admin 💠"
        admin_role_id = 266701171002048513

        verified_role_name = "Verified 🔰"
        verified_role_id = 366739104203014145

        pokemon_channel = 439198154324181002
        accept_channel = 356456207185215491
        canvas_channel = 482084251702132746

        mute_role_id = 363900817805148160
        mute_role_name = "Text Muted"
        shut_up_role = 414245504537591810

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

        # Group Roles (games.py)
        groups_message_id = 495070906906050560
        code_role = 494998056794849290
        boof_role = 370723456607715330
        max_role = 420706263895375892
        path_role = 491707496767946753
        poker_role = 442837936552017930
        dj_role = 397440571293040641
        snowboard_role = 378342844282306581

        return
    else:
        sys.exit("No Server (main/test)")

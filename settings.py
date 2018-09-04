#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import discord
import logging
import subprocess


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
        mute_role_name, embed_color, server_name, accept_channel, canvas_channel
    embed_color = 0x593595

    if server == "test":
        print("Using TEST account")
        jsontoken = get_json('tokens.json')
        token = jsontoken.get("test")
        upvote_emoji = ":upvote:414204250642579488"
        downvote_emoji = ":downvote:414204250948894721"
        notification_channel = 414974032048553984
        member_role_id = 414683704737267712
        member_role_name = "Member ðŸ”¸"
        shut_up_role = 414237651504332800
        admin_role_name = "Admin ðŸ’ "
        admin_role_id = 439175903600181269
        verified_role_name = "Verified ðŸ”°"
        verified_role_id = 439191092991229992
        pokemon_channel = 439198154324181002
        mute_role_id = 445059188973109259
        mute_role_name = "Text Muted"
        server_name = "test"
        accept_channel = None
        canvas_channel = 484772795687895041
        return
    if server == "main":
        print("Using MAIN account")
        jsontoken = get_json('tokens.json')
        token = jsontoken.get("main")
        upvote_emoji = ":upvote:412119803034075157"
        downvote_emoji = ":downvote:412119802904313858"
        notification_channel = 412075980094570506
        member_role_id = 312693233329373194
        member_role_name = "Member ðŸ”¸"
        admin_role_name = "Admin ðŸ’ "
        admin_role_id = 266701171002048513
        shut_up_role = 414245504537591810
        verified_role_name = "Verified ðŸ”°"
        verified_role_id = 366739104203014145
        pokemon_channel = 439198154324181002
        mute_role_id = 363900817805148160
        mute_role_name = "Text Muted"
        server_name = "main"
        accept_channel = 356456207185215491
        canvas_channel = 482084251702132746
    else:
        sys.exit("No Server (main/test)")

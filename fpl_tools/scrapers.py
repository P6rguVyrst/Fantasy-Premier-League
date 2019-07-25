#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .getters import (
    get_entry_data,
    get_entry_personal_data,
    get_data,
    get_individual_player_data,
    get_fixtures_data,
)
from .parsers import (
    parse_entry_history,
    parse_entry_leagues,
    parse_players,
    parse_team_data,
    parse_player_history,
    parse_player_gw_history,
    parse_fixtures,
)
from .cleaners import (
    clean_players,
    id_players,
    get_player_ids,
)
from .collector import collect_gw, merge_gw
from .exceptions import TeamIdError
import sys
import os


def team_scraper(season, team_id):

    if not team_id:
        raise TeamIdError("Usage: python teams_scraper.py <team_id>. Eg: python teams_scraper.py 5000")

    output_folder = "archive/team_{}_data{}".format(team_id, season)
    assert_output_folder_exists(output_folder)

    summary = get_entry_data(team_id)
    personal_data = get_entry_personal_data(team_id)
    # The link does not seem to be providing the right information
    #gws = get_entry_gws_data(team_id)
    #transfers = get_entry_transfers_data(team_id)
    parse_entry_history(summary, output_folder)
    parse_entry_leagues(personal_data, output_folder)
    #parse_transfer_history(transfers, output_folder)
    #parse_gw_entry_history(gws, output_folder)


def assert_output_folder_exists(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def global_scraper(**kwargs):
    """ Parse and store all the data
    """
    data = get_data("https://fantasy.premierleague.com/api/bootstrap-static/")
    season = '2019-20'
    base_filename = 'data/{}/'.format(season)

    parse_players(data["elements"], base_filename)

    try:
        gw_num = data["current-event"]
    except Exception:
        gw_num = 0

    clean_players(base_filename + 'players_raw.csv', base_filename)
    fixtures(base_filename)

    if gw_num == 0:
        parse_team_data(data["teams"], base_filename)

    id_players(base_filename + 'players_raw.csv', base_filename)
    player_ids = get_player_ids(base_filename)

    player_base_filename = base_filename + 'players/'
    gw_base_filename = base_filename + 'gws/'

    for player_id in range(len(data["elements"])):
        player_id += 1
        player_data = get_individual_player_data(player_id)
        parse_player_history(
            player_data["history_past"],
            player_base_filename,
            player_ids[player_id],
            player_id,
        )
        parse_player_gw_history(
            player_data["history"],
            player_base_filename,
            player_ids[player_id],
            player_id,
        )

    if gw_num > 0:
        collect_gw(gw_num, player_base_filename, gw_base_filename)
        merge_gw(gw_num, gw_base_filename)


def fixtures(base_filename):
    data = get_fixtures_data()
    parse_fixtures(data, base_filename)

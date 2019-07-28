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
    parse_players,
    parse_team_data,
    parse_player_history,
    parse_player_gw_history,
    parse_fixtures,
    write_to_csv,
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
from pandas import DataFrame


def team_scraper(**kwargs):

    season = kwargs.get("season")
    team_id = kwargs.get("team")

    if not team_id:
        raise TeamIdError("Usage: fpl teams -t 5000")

    output_folder = "archive/team_{}_data{}".format(team_id, season)
    assert_output_folder_exists(output_folder)

    entrant_summary = get_entry_data(team_id)
    write_to_csv(
        entrant_summary.get("chips"),
        '{}/chips.csv'.format(output_folder)
    )
    write_to_csv(
        entrant_summary.get("past"),
        '{}/history.csv'.format(output_folder)
    )
    write_to_csv(
        entrant_summary.get("current"),
        '{}/gws.csv'.format(output_folder)
    )


    personal_data = get_entry_personal_data(team_id)
    write_to_csv(
        personal_data["leagues"].get("classic"),
        '{}/classic_leagues.csv'.format(output_folder)
    )
    write_to_csv(
        personal_data["leagues"].get("h2h"),
        '{}/h2h_leagues.csv'.format(output_folder)
    )
    write_to_csv(
        personal_data["leagues"].get("cup"),
        '{}/cup_leagues.csv'.format(output_folder)
    )

    # The link does not seem to be providing the right information
    # gws = get_entry_gws_data(team_id)
    # transfers = get_entry_transfers_data(team_id)
    # parse_transfer_history(transfers, output_folder)
    # parse_gw_entry_history(gws, output_folder)


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
            player_data.get("history_past"),
            player_base_filename,
            player_ids.get(player_id),
            player_id,
        )
        parse_player_gw_history(
            player_data.get("history"),
            player_base_filename,
            player_ids.get(player_id),
            player_id,
        )

    if gw_num > 0:
        collect_gw(gw_num, player_base_filename, gw_base_filename)
        merge_gw(gw_num, gw_base_filename)


def fixtures(base_filename):
    data = get_fixtures_data()
    parse_fixtures(data, base_filename)

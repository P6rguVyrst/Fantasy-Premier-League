#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .getters import get_entry_data, get_entry_personal_data
from .parsers import parse_entry_history, parse_entry_leagues
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

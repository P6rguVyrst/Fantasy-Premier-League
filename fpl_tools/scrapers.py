#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .parsers import Asset
from .collector import collect_gw, merge_gw
from .exceptions import TeamIdError
from .utils import APIClient
import os
import pandas as pd


class FPLClient:

    def __init__(self, fpl_api, output_dir):
        self.api = APIClient(fpl_api)
        self.output_dir = output_dir

    def write_to_csv(self, data, output_file, index=True):
        if data:
            pd.DataFrame.from_records(data).to_csv(output_file, index=index)
        else:
            print('No data for {}'.format(output_file))

    def assert_folder_exists(self, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def team_scraper(self, **kwargs):

        season = kwargs.get("season")
        team_id = kwargs.get("team")

        if not team_id:
            raise TeamIdError("Usage: fpl team --team-id 5000")

        self.assert_folder_exists("archive/team_{}_data{}".format(team_id, season))

        entrant_summary = self.api.get("entry/{}/history".format(team_id)).json()
        personal_data = self.api.get("entry/{}".format(team_id)).json()

        fpl_data = {
            'chips.csv': entrant_summary.get("chips"),
            'history.csv': entrant_summary.get("past"),
            'gws.csv': entrant_summary.get("current"),
            'classic_leagues.csv': personal_data["leagues"].get("classic"),
            'h2h_leagues.csv': personal_data["leagues"].get("h2h"),
            'cup_leagues.csv': personal_data["leagues"].get("cup"),
        }

        for output_file, data in fpl_data.items():
            self.write_to_csv(data, 'archive/team_{}_data{}/{}'.format(team_id, season, output_file))


    def global_scraper(self, **kwargs):
        """ Parse and store all the data
        """
        # How should I pass a dummy API here
        data = self.api.get("bootstrap-static/").json()
        self._global_parser(data)

    def _global_parser(self, data):

        # TODO: fix fx input params.
        push = Asset(data, self.output_dir)
        push.parse_players()
        push.id_players()

        for player_id in range(len(data["elements"])):
            player_id += 1
            endpoint = "element-summary/{}".format(player_id)
            player_data = self.api.get(endpoint).json()
            push.parse_player_history(player_data.get("history_past"), player_id)
            push.parse_player_gw_history(player_data.get("history"), player_id)

        fixtures = self.api.get("fixtures/").json()
        output_file = '{}/fixtures.csv'.format(self.output_dir)
        self.write_to_csv(fixtures, output_file, index=False)

        gw_num = data.get("current-event", 0)
        if gw_num == 0:
            output_file = '{}/teams.csv'.format(self.output_dir)
            self.write_to_csv(data["teams"], output_file, index=False)
        if gw_num > 0:
            collect_gw(gw_num, self.output_dir)
            merge_gw(gw_num, self.output_dir + "gws/")

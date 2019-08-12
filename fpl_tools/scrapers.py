#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .parsers import (
    Asset,
    parse_team_data,
    parse_player_history,
    parse_player_gw_history,
    parse_fixtures,
    write_to_csv,
)
from .collector import collect_gw, merge_gw
from .exceptions import TeamIdError
from .utils import APIClient, assert_folder_exists


class FPLClient:

    def __init__(self, fpl_api):
        self.api = APIClient(fpl_api)

    def team_scraper(self, **kwargs):

        season = kwargs.get("season")
        team_id = kwargs.get("team")
        output_folder = kwargs.get("dir")

        if not team_id:
            raise TeamIdError("Usage: fpl team --team-id 5000")

        assert_folder_exists("archive/team_{}_data{}".format(team_id, season))

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
            write_to_csv(data, '{}/{}'.format(output_folder, output_file))


    def global_scraper(self, **kwargs):
        """ Parse and store all the data
        """
        # How should I pass a dummy API here
        output_folder = kwargs.get("dir")
        data = self.api.get("bootstrap-static/").json()
        self._global_parser(data, output_folder)

    def _global_parser(self, data, output_folder):

        # TODO: fix fx input params.
        push = Asset(data, output_folder)
        push.parse_players()
        push.id_players()

        player_ids = push.get_player_ids()

        for player_id in range(len(data["elements"])):
            player_id += 1
            endpoint =  "element-summary/{}".format(player_id)
            player_data = self.api.get(endpoint).json()
            parse_player_history(
                player_data.get("history_past"),
                '{}/players/'.format(output_folder),
                player_ids.get(player_id),
                player_id,
            )
            parse_player_gw_history(
                player_data.get("history"),
                '{}/players/'.format(output_folder),
                player_ids.get(player_id),
                player_id,
            )

        self._assets(data, output_folder)
        self._fixtures(output_folder)

        gw_num = data.get("current-event", 0)
        if gw_num == 0:
            parse_team_data(data["teams"], output_folder)
        if gw_num > 0:
            collect_gw(gw_num, output_folder)
            merge_gw(gw_num, gw_output_folder)

    def _fixtures(self, output_folder):
        fixtures = self.api.get("fixtures/").json()
        parse_fixtures(fixtures, output_folder)

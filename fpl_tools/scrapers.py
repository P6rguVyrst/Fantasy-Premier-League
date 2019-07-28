#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from .utils import APIClient, assert_folder_exists


class FPLClient:

    def __init__(self, fpl_api):
        self.api = APIClient(fpl_api)

    def team_scraper(self, **kwargs):

        season = kwargs.get("season")
        team_id = kwargs.get("team")

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

        for output_file, data in fpl_data:
            write_to_csv(data, '{}/{}'.format(output_folder, output_file))

        # The link does not seem to be providing the right information
        # gws = get_entry_gws_data(team_id)
        # endpoint = "entry/{}/transfers".format(team_id)
        # transfers = self.api.get(endpoint).json()
        # parse_transfer_history(transfers, output_folder)
        # parse_gw_entry_history(gws, output_folder)

    def global_scraper(self, **kwargs):
        """ Parse and store all the data
        """
        season = kwargs.get("season")
        output_folder = 'data/{}/'.format(season)

        data = self.api.get("bootstrap-static/").json()

        parse_players(data["elements"], output_folder)
        clean_players('players_raw.csv', output_folder)

        self._fixtures(output_folder)

        gw_num = data.get("current-event", 0)

        if gw_num == 0:
            parse_team_data(data["teams"], output_folder)

        self._assets(data, output_folder)

        if gw_num > 0:
            collect_gw(gw_num, player_output_folder, '{}/gws/'.format(output_folder))
            merge_gw(gw_num, gw_output_folder)

    def _fixtures(self, output_folder):
        fixtures = self.api.get("fixtures/").json()
        parse_fixtures(fixtures, output_folder)

    def _assets(self, data, output_folder):
        id_players('players_raw.csv', output_folder)
        player_ids = get_player_ids(output_folder)
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

    #FIXIT: unused, get rid of the list. deprecated api endpoint.
    def get_entry_gws_data(self, entry_id):
        """ Retrieve the gw-by-gw data for a specific entry/team

        Args:
            entry_id (int) : ID of the team whose data is to be retrieved
        """
        base_url = "https://fantasy.premierleague.com/api/entry/"
        gw_data = []
        for i in range(1, 39):
            endpoint = "entry/{}/event/{}".format(entry_id, i)
            response = api.get(endpoint).json()
            gw_data += [response]
        return response

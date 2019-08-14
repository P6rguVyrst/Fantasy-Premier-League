#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os


class Asset:

    def __init__(self, player_data, output_dir):
        self.player_data = player_data
        self.output_dir = output_dir

    def _ensure_file(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _extract_stat_names(self, dict_of_stats):
        return list(dict_of_stats.keys())

    def id_players(self):
        """ Creates a file that contains the name to id mappings for each player
        """
        headers = ['first_name', 'second_name', 'id']
        players_raw = self.output_dir + 'players_raw.csv'
        outname = self.output_dir + 'player_idlist.csv'

        fin = open(players_raw, 'r+', encoding='utf-8')
        self._ensure_file(outname)
        fout = open(outname, 'w+', encoding='utf-8', newline='')
        writer = csv.DictWriter(fout, headers, extrasaction='ignore')
        writer.writeheader()

        for line in csv.DictReader(fin):
            writer.writerow(line)

    def _get_player_ids(self):
        """ Gets the list of all player ids and player names
        """
        filename = self.output_dir + 'player_idlist.csv'
        fin = open(filename, 'r+', encoding='utf-8')
        reader = csv.DictReader(fin)
        player_ids = {}
        for line in reader:
            k = int(line['id'])
            v = line['first_name'] + '_' + line['second_name']
            player_ids[k] = v
        return player_ids

    def parse_players(self):
        stat_names = self._extract_stat_names(
            self.player_data["elements"][0]
        )
        filename = self.output_dir + 'players_raw.csv'
        self._ensure_file(filename)

        # TODO: context manager, with open.
        f = open(filename, 'w+', encoding='utf8', newline='')
        w = csv.DictWriter(f, sorted(stat_names))
        w.writeheader()
        for player in self.player_data["elements"]:
                w.writerow({k: str(v).encode('utf-8').decode('utf-8') for k, v in player.items()})
        self.clean_players()

    def clean_players(self):
        """ Creates a file with only important data columns for each player
        """
        headers = [
            'first_name', 'second_name', 'goals_scored',
            'assists', 'total_points', 'minutes',
            'goals_conceded', 'creativity', 'influence',
            'threat', 'bonus', 'bps', 'ict_index',
            'clean_sheets', 'red_cards', 'yellow_cards',
            'selected_by_percent', 'now_cost'
        ]
        players_raw = self.output_dir + 'players_raw.csv'
        fin = open(players_raw, 'r+', encoding='utf-8')

        outname = self.output_dir + 'cleaned_players.csv'
        self._ensure_file(outname)
        fout = open(outname, 'w+', encoding='utf-8', newline='')
        writer = csv.DictWriter(fout, headers, extrasaction='ignore')
        writer.writeheader()
        for line in csv.DictReader(fin):
            writer.writerow(line)

    def parse_player_history(self, list_of_histories, _id):
        player_name = self._get_player_ids().get(_id)
        if list_of_histories:
            stat_names = self._extract_stat_names(list_of_histories[0])
            filename = self.output_dir + 'players/' + player_name + '_' + str(_id) + '/history.csv'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            f = open(filename, 'w+', encoding='utf8', newline='')
            w = csv.DictWriter(f, sorted(stat_names))
            w.writeheader()
            for history in list_of_histories:
                w.writerow(history)

    def parse_player_gw_history(self, list_of_gw, _id):
        player_name = self._get_player_ids().get(_id)
        if list_of_gw:
            stat_names = self._extract_stat_names(list_of_gw[0])
            filename = self.output_dir + 'players/' + player_name + '_' + str(_id) + '/gw.csv'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            f = open(filename, 'w+', encoding='utf8', newline='')
            w = csv.DictWriter(f, sorted(stat_names))
            w.writeheader()
            for gw in list_of_gw:
                w.writerow(gw)

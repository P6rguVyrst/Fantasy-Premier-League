import csv
import os
from .utility import uprint
import pandas as pd


def extract_stat_names(dict_of_stats):
    """ Extracts all the names of the statistics

    Args:
        dict_of_stats (dict): Dictionary containing key-alue pair of stats
    """
    stat_names = []
    for key, val in dict_of_stats.items():
        stat_names += [key]
    return stat_names

def parse_players(list_of_players, base_filename):
    stat_names = extract_stat_names(list_of_players[0])
    filename = base_filename + 'players_raw.csv'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w+', encoding='utf8', newline='')
    w = csv.DictWriter(f, sorted(stat_names))
    w.writeheader()
    for player in list_of_players:
            w.writerow({k:str(v).encode('utf-8').decode('utf-8') for k, v in player.items()})

def parse_player_history(list_of_histories, base_filename, player_name, Id):
    if list_of_histories:
        stat_names = extract_stat_names(list_of_histories[0])
        filename = base_filename + player_name + '_' + str(Id) + '/history.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, 'w+', encoding='utf8', newline='')
        w = csv.DictWriter(f, sorted(stat_names))
        w.writeheader()
        for history in list_of_histories:
            w.writerow(history)

def parse_player_gw_history(list_of_gw, base_filename, player_name, Id):
    if list_of_gw:
        stat_names = extract_stat_names(list_of_gw[0])
        filename = base_filename + player_name + '_' + str(Id) + '/gw.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, 'w+', encoding='utf8', newline='')
        w = csv.DictWriter(f, sorted(stat_names))
        w.writeheader()
        for gw in list_of_gw:
            w.writerow(gw)

def parse_gw_entry_history(data, output_folder):
    i = 1
    for gw in data:
        print(gw)
        i += 1


def write_to_csv(data, output_file):
    if data:
        pd.DataFrame.from_records(data).to_csv(output_file)
    else:
        print('No data for {}'.format(output_file))


def parse_transfer_history(data, output_folder):
    pd.DataFrame.from_records(data["wildcards"]).to_csv(
        '{}/wildcards.csv'.format(output_folder)
    )
    pd.DataFrame.from_records(data["history"]).to_csv(
        '{}/transfers.csv'.format(output_folder)
    )


def parse_fixtures(data, output_folder):
    pd.DataFrame.from_records(data).to_csv(
        '{}/fixtures.csv'.format(output_folder), index=False
    )


def parse_team_data(data, output_folder):
    pd.DataFrame.from_records(data).to_csv(
        '{}/teams.csv'.format(output_folder), index=False
    )

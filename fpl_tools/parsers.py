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
    if len(list_of_histories) > 0:
        stat_names = extract_stat_names(list_of_histories[0])
        filename = base_filename + player_name + '_' + str(Id) + '/history.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, 'w+', encoding='utf8', newline='')
        w = csv.DictWriter(f, sorted(stat_names))
        w.writeheader()
        for history in list_of_histories:
            w.writerow(history)

def parse_player_gw_history(list_of_gw, base_filename, player_name, Id):
    if len(list_of_gw) > 0:
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


def parse_entry_history(data, output_folder):
    # TODO: rename, get rid of os path here.
    pd.DataFrame.from_records(data["chips"]).to_csv(
        'chips.csv'.format(output_folder))
    )
    pd.DataFrame.from_records(data["past"]).to_csv(
        '{}/history.csv'.format(output_folder))
    )
    pd.DataFrame.from_records(data["current"]).to_csv(
        '{}/gws.csv'.format(output_folder))
    )
    #profile_data = data["entry"].pop('kit', data["entry"])
    #profile_df = pd.DataFrame.from_records(profile_data)
    #profile_df.to_csv(os.path.join(output_folder, 'profile.csv'))


def parse_entry_leagues(data, output_folder):
    # TODO: fixit, assumptions that some keys may exist, some not.
    pd.DataFrame.from_records(data["leagues"]["classic"]).to_csv(
        '{}/classic_leagues.csv'.format(output_folder))
    )
    pd.DataFrame.from_records(data["leagues"]["h2h"]).to_csv(
        '{}/h2h_leagues.csv'.format(output_folder))
    )
    try:
        pd.DataFrame.from_records(data["leagues"]["cup"]).to_csv(
            '{}/cup_leagues.csv'.format(output_folder))
        )
    except KeyError:
        print("No cups yet")


def parse_transfer_history(data, output_folder):
    pd.DataFrame.from_records(data["wildcards"]).to_csv(
        '{}/wildcards.csv'.format(output_folder))
    )
    pd.DataFrame.from_records(data["history"]).to_csv(
        '{}/transfers.csv'.format(output_folder))
    )


def parse_fixtures(data, output_folder):
    pd.DataFrame.from_records(data).to_csv(
        '{}/fixtures.csv'.format(output_folder)), index=False
    )


def parse_team_data(data, output_folder):
    pd.DataFrame.from_records(data).to_csv(
        '{}/teams.csv'.format(output_folder)), index=False
    )

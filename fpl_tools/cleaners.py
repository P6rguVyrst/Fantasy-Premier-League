import csv
import math
import os

def clean_players(filename, output_folder):
    """ Creates a file with only important data columns for each player

    Args:
        filename (str): Name of the file that contains the full data for each player
    """
    headers = [
        'first_name', 'second_name', 'goals_scored',
        'assists', 'total_points', 'minutes',
        'goals_conceded', 'creativity', 'influence',
        'threat', 'bonus', 'bps', 'ict_index',
        'clean_sheets', 'red_cards', 'yellow_cards',
        'selected_by_percent', 'now_cost'
    ]
    players_raw = output_folder + filename
    fin = open(players_raw, 'r+', encoding='utf-8')

    outname = output_folder + 'cleaned_players.csv'
    os.makedirs(os.path.dirname(outname), exist_ok=True)
    fout = open(outname, 'w+', encoding='utf-8', newline='')
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, headers, extrasaction='ignore')
    writer.writeheader()
    for line in reader:
        writer.writerow(line)

def id_players(filename, output_folder):
    """ Creates a file that contains the name to id mappings for each player

    Args:
        filename (str): Name of the file that contains the full data for each player
    """
    headers = ['first_name', 'second_name', 'id']
    players_raw = output_folder + filename
    fin = open(players_raw, 'r+', encoding='utf-8')
    outname = output_folder + 'player_idlist.csv'
    os.makedirs(os.path.dirname(outname), exist_ok=True)
    fout = open(outname, 'w+', encoding='utf-8', newline='')
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, headers, extrasaction='ignore')
    writer.writeheader()
    for line in reader:
        writer.writerow(line)

def get_player_ids(output_folder):
    """ Gets the list of all player ids and player names
    """
    filename = output_folder + 'player_idlist.csv'
    fin = open(filename, 'r+', encoding='utf-8')
    reader = csv.DictReader(fin)
    player_ids = {}
    for line in reader:
        k = int(line['id'])
        v = line['first_name'] + '_' + line['second_name']
        player_ids[k] = v
    return player_ids

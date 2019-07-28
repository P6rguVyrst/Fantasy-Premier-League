#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests.exceptions import RequestException
import logging
import requests
import json
import time
import sys


LOGGER = logging.getLogger(__name__)


def get_data(url):
    """ Retrieve the fpl player data from the hard-coded url
    """
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        LOGGER.warning("Response code: {}".format(response.status_code))
        return response.json()

def get_data_retry(url):
    #response = False
    #while not response:
    #    try:
    #        response = get_data(url)
    #    except:
    #        time.sleep(5)
    #return response
    return get_data(url)


def get_individual_player_data(player_id):
    """ Retrieve the player-specific detailed data

    Args:
        player_id (int): ID of the player whose data is to be retrieved
    """
    full_url = "{}/{}".format("https://fantasy.premierleague.com/api/element-summary", player_id)
    return get_data_retry(full_url)


def get_entry_data(entry_id):
    """ Retrieve the summary/history data for a specific entry/team

    Args:
        entry_id (int) : ID of the team whose data is to be retrieved
    """
    full_url = "{}/{}/history".format("https://fantasy.premierleague.com/api/entry", entry_id)
    return get_data_retry(full_url)


def get_entry_personal_data(entry_id):
    """ Retrieve the summary/history data for a specific entry/team

    Args:
        entry_id (int) : ID of the team whose data is to be retrieved
    """
    full_url = "{}/{}".format("https://fantasy.premierleague.com/api/entry", entry_id)
    return get_data_retry(full_url)


#FIXIT: unused, get rid of the list. deprecated api endpoint.
def get_entry_gws_data(entry_id):
    """ Retrieve the gw-by-gw data for a specific entry/team

    Args:
        entry_id (int) : ID of the team whose data is to be retrieved
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    gw_data = []
    for i in range(1, 39):
        full_url = base_url + str(entry_id) + "/event/" + str(i)
        response = get_data_retry(full_url)
        gw_data += [response]
    return response


def get_entry_transfers_data(entry_id):
    """ Retrieve the transfer data for a specific entry/team

    Args:
        entry_id (int) : ID of the team whose data is to be retrieved
    """
    full_url = "{}/{}/transfers".format("https://fantasy.premierleague.com/api/entry", entry_id)
    return get_data_retry(full_url)

def get_fixtures_data():
    """ Retrieve the fixtures data for the season
    """
    url = "https://fantasy.premierleague.com/api/fixtures/"
    return get_data_retry(url)


def deprecated_getter(**kwargs):
    data = get_data("https://fantasy.premierleague.com/api/bootstrap-static/")
    with open('raw.json', 'w') as outf:
        json.dump(data, outf)

from fpl_tools.getters import (
    get_data,
    get_individual_player_data,
    get_entry_data,
    get_entry_personal_data,
    get_entry_gws_data,
    get_entry_transfers_data,
    get_fixtures_data,
)
from pprint import pprint as pp
import pytest


def test_get_data():
    """bootstrap-static"""
    bootstrap_static = get_data("https://fantasy.premierleague.com/api/bootstrap-static/")
    assert isinstance(bootstrap_static, dict)


def test_get_individual_player_data():
    """element-summary/{player-id}"""
    element_summary = get_individual_player_data(234)
    assert isinstance(element_summary, dict)


def test_get_entry_data():
    """entry/{entry-id}/history"""
    entry_history = get_entry_data(234)
    assert isinstance(entry_history, dict)


def test_get_entry_personal_data():
    """entry/{entry-id}"""
    entry_personal = get_entry_personal_data(234)
    assert isinstance(entry_personal, dict)


@pytest.mark.skip(reason="Deprecated endpoint.")
def test_get_entry_gws_data():
    """entry/{entry-id}/event/{gameweek}"""
    entry_gws = get_entry_gws_data(234)
    assert isinstance(entry_gws, dict)


@pytest.mark.skip(reason="Deprecated endpoint.")
def test_get_entry_transfers_data():
    """entry/{entry-id}/transfers}"""
    entry_transfers = get_entry_transfers_data(234)
    assert isinstance(entry_transfers, dict)


def test_get_fixtures_data():
    """fixtures"""
    fixtures = get_fixtures_data()
    assert isinstance(fixtures, list)
    pp(fixtures)

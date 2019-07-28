from pprint import pprint as pp
import pytest


def test_get_data(api_client_fixture, bootstrap_static_fixture):
    # bootstrap_static = get_data("https://fantasy.premierleague.com/api/bootstrap-static/")
    response = api_client_fixture.get(
        "/bootstrap-static/",
        response_body=bootstrap_static_fixture
    ).json()
    #pp(response)
    assert isinstance(response, dict)


def test_get_individual_player_data(api_client_fixture, element_summary_fixture):
    # element_summary = get_individual_player_data(234)
    response = api_client_fixture.get(
        "/element-summary/234/",
        response_body=element_summary_fixture
    ).json()
    assert isinstance(response, dict)


def test_get_entry_data(api_client_fixture, entry_fixture_history):
    # entry_history = get_entry_data(234)
    response = api_client_fixture.get(
        "/entry/234/history/",
        response_body=entry_fixture_history
    ).json()
    assert isinstance(response, dict)


def test_get_entry_personal_data(api_client_fixture, entry_fixture):
    # entry_personal = get_entry_personal_data(234)
    response = api_client_fixture.get(
        "/entry/234/",
        response_body=entry_fixture
    ).json()
    assert isinstance(response, dict)


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


def test_get_fixtures_data(api_client_fixture, fixtures):
    """fixtures"""
    # fixtures = get_fixtures_data()
    response = api_client_fixture.get(
        "/fixtures/",
        response_body=fixtures
    ).json()
    assert isinstance(response, list)

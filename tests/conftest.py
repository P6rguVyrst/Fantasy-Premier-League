import json
import pytest
import responses
import requests


class APIFixture():

    def __init__(self):
        self.api = "https://asd.foobssdgef.iot/api"

    @responses.activate
    def get(self, endpoint, response_status=200, response_body=None):
        url = self.api + endpoint
        responses.add(responses.GET, url, status=response_status, json=response_body)
        response = requests.get(url)
        return response


@pytest.fixture
def api_client_fixture(scope="session"):
    mock_api_client = APIFixture()
    return mock_api_client


@pytest.fixture
def entry_fixture(scope="session"):
    with open("tests/data/entry_234.json") as data:
        res = json.load(data)
    return res


@pytest.fixture
def entry_fixture_history(scope="session"):
    with open("tests/data/entry_234_history.json") as data:
        res = json.load(data)
    return res


@pytest.fixture
def bootstrap_static_fixture(scope="session"):
    with open("tests/data/bootstrap-static.json") as data:
        res = json.load(data)
    return res


@pytest.fixture
def element_summary_fixture(scope="session"):
    with open("tests/data/element-summary_234.json") as data:
        res = json.load(data)
    return res


@pytest.fixture
def fixtures(scope="session"):
    with open("tests/data/fixtures.json") as data:
        res = json.load(data)
    return res

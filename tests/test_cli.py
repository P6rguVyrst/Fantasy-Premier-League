import pytest
from click.testing import CliRunner
from fpl_tools import cli

runner = CliRunner()


def test_cli_team_success():
    result = runner.invoke(cli.main, ["team", "-t", "5000"])
    assert result.exit_code == 0


def test_cli_success():
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0


#@pytest.mark.xfail
#@pytest.mark.skip(reason="Takes too long to run.")
def test_cli_global_success():
    """Because of REAL, API calls, takes too long to run.
    Replace with APICLientFactory, that will return dummy fixture for testing?
    """
    result = runner.invoke(cli.main, ["global"])
    assert result.exit_code == 0

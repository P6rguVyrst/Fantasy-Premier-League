#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI for interacting with FPL tools."""


import sys
import click
from .scrapers import team_scraper


@click.command()
@click.argument("mode")
@click.option("-s", "--season", default="19_20", help="Premier League season")
@click.option("-t", "--team-id", help="USAGE: fpl team --team-id=5000")
def main(mode, season, team_id):

    mode_router = {
        "team": team_scraper,
    }

    allowed_modes = mode_router.keys()

    if mode not in allowed_modes:
        raise NotImplementedError("mode: {} - not implemented, available arguments: {}".format(mode, allowed_modes))

    mode_router[mode](season=season, team_id=team_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())

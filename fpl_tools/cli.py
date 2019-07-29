#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI for interacting with FPL tools."""


import sys
import logging
import click
from .scrapers import FPLClient
from .collector import merge_all_gws, collect_all_gws


@click.command()
@click.argument("mode")
@click.option("-t", "--team-id", help="USAGE: fpl team --team-id=5000")
@click.option("-g", "--gw-count", help="")
@click.option("-f", "--output-dir", default="data/19_20/", help="Output directory")
def main(mode, team_id, gw_count, output_dir):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    client = FPLClient("https://fantasy.premierleague.com/api/")

    mode_router = {
        "team": client.team_scraper,
        "global": client.global_scraper,
        "merge-gw": merge_all_gws,
        "collect-gw": collect_all_gws, # IMPLEMENT
    }

    allowed_modes = mode_router.keys()

    if mode not in allowed_modes:
        raise NotImplementedError("mode: {} - not implemented, available arguments: {}".format(mode, allowed_modes))

    kwargs = dict()
    kwargs["team"] = team_id
    kwargs["gw"] = gw_count
    kwargs["dir"] = output_dir

    mode_router[mode](**kwargs)

    return 0


if __name__ == "__main__":
    sys.exit(main())

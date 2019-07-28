#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI for interacting with FPL tools."""


import sys
import logging
import click
from .scrapers import team_scraper, global_scraper
from .collector import merge_all_gws, collect_all_gws
from .getters import deprecated_getter


@click.command()
@click.argument("mode")
@click.option("-s", "--season", default="19_20", help="Premier League season")
@click.option("-t", "--team-id", help="USAGE: fpl team --team-id=5000")
@click.option("-g", "--gw-count", help="")
@click.option("-f", "--output-dir", help="Output directory")
def main(mode, season, team_id, gw_count, output_dir):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    mode_router = {
        "team": team_scraper,
        "global": global_scraper,
        "merge-gw": merge_all_gws,  # FIXIT: params. argv1 argv2
        "collect-gw": collect_all_gws, # IMPLEMENT
        "get-data":  deprecated_getter,
    }

    allowed_modes = mode_router.keys()

    if mode not in allowed_modes:
        raise NotImplementedError("mode: {} - not implemented, available arguments: {}".format(mode, allowed_modes))

    kwargs = dict()
    kwargs["season"] = season
    kwargs["team"] = team_id
    kwargs["gw"] = gw_count
    kwargs["dir"] = output_dir

    mode_router[mode](**kwargs)

    return 0


if __name__ == "__main__":
    sys.exit(main())

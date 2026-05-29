# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click>=8.4.1",
#     "rich>=15.0.0",
#     "polars>=1.40.1",
#     "rustworkx>=0.17.1"
# ]
# ///
import sys, io
import click

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

import polars as pl
from carousel import match_from_prefs


@click.command()
@click.argument("preferences", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--show-preferences",
    "-b",
    is_flag=True,
    help="Show relevant preferences (after selections).",
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty-print output.")
def cli(preferences: str, show_ballots=False, pretty=False) -> None:
    """
    Compute the Gale-Shapley stable match of some preferences -- .csv or .xls(x).

    A stable matching (of the "college admissions" problem) is one in which there is no
    pair of, say, TA and course which would prefer each other over their respective
    assignment given by the matching.
    """

    console = Console()

    pass


if __name__ == "__main__":
    cli()

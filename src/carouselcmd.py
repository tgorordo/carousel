# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click>=8.4.1",
#     "rich>=15.0.0",
#     "polars>=1.40.1",
# ]
# ///
import sys, io
import click

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

import polars as pl
from carousel import default_convranks, default_caps, def_acc_GS


@click.command()
@click.argument("applicant-prefs", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--position-prefs", type=click.Path(exists=True, dir_okay=False), default=None
)
@click.option("--capacities", type=str, default=None)
@click.option("--app-col", default="applicant")
@click.option("--pos-col", default="position")
@click.option("--rnk-col", default="rank")
@click.option(
    "--show-prefs",
    "-b",
    is_flag=True,
    help="Show relevant preferences (after selections).",
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty-print output.")
def cli(
    applicant_prefs: str,
    position_prefs: str | None,
    capacities: str | None,
    app_col: str,
    pos_col: str,
    rnk_col: str,
    show_prefs: bool,
    pretty: bool,
) -> None:
    """
    Compute the Gale-Shapley stable match of some preferences -- .csv or .xls(x).

    A stable matching (of the "college admissions" problem) is one in which there is no
    pair of, say, TA and course which would prefer each other over their respective
    assignment given by the matching.
    """

    console = Console()

    try:
        if applicant_prefs.endswith(".csv"):
            dfa = pl.read_csv(applicant_prefs)
        elif applicant_prefs.endswith((".xlsx", ".xls")):
            dfa = pl.read_excel(applicant_prefs)
        else:
            console.print(
                "[bold red]Unsupported applicant_prefs filetype.[/bold red]\nUse CSV or Excel."
            )
            raise SystemExit(1)

        dfa = dfa.rename({c: c.strip() for c in dfa.columns})
        dfa = dfa.with_columns(
            [pl.col(app_col).cast(pl.Utf8).str.strip_chars()]
            + [
                pl.col(c).cast(pl.Utf8).str.strip_chars().cast(pl.Int64, strict=False)
                for c in dfa.columns
                if c != app_col
            ]
        )

        if position_prefs is None:
            dfp = default_convranks(dfa, app_col, pos_col)
        elif position_prefs.endswith(".csv"):
            dfp = pl.read_csv(position_prefs)
        elif position_prefs.endswith((".xlsx", ".xls")):
            dfp = pl.read_excel(position_prefs)
        else:
            console.print(
                "[bold red]Unsupported position_prefs filetype.[/bold red]\nUse CSV or Excel."
            )
            raise SystemExit(1)

        dfp = dfp.rename({c: c.strip() for c in dfp.columns})
        dfp = dfp.with_columns(
            [pl.col(pos_col).cast(pl.Utf8).str.strip_chars()]
            + [
                pl.col(c).cast(pl.Utf8).str.strip_chars().cast(pl.Int64, strict=False)
                for c in dfp.columns
                if c != pos_col
            ]
        )

        if capacities is None:
            caps = default_caps(dfp)
        elif capacities.endswith(".csv"):
            caps = pl.read_csv(capacities)
        elif capacities.endswith((".xlsx", ".xls")):
            caps = pl.read_excel(capacities)
        else:
            positions = dfp[pos_col].to_list()
            caps = [int(x.strip()) for x in capacities.split(",")]

            if len(caps) != len(positions):
                raise click.ClickException(
                    f"Expected {len(positions)} capacities, found {len(caps)}."
                )

            caps = pl.DataFrame({pos_col: positions, "capacity": caps})

        match = def_acc_GS(
            dfa, dfp, caps, app_col=app_col, pos_col=pos_col, rank_col=rnk_col
        )

        if pretty:
            t = Table(title="GS Matching")

            for col in match.columns:
                t.add_column(col)

            for row in match.iter_rows():
                t.add_row(*map(str, row))

            console.print(t)
            console.print()
        else:
            for row in match.iter_rows():
                console.print(", ".join(f"{c}" for c in map(str, row)))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    cli()

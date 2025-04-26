import logging, rich
from rich.logging import RichHandler

rich.traceback.install()

import itertools as it
import numpy as np

import polars as pl
import polars.selectors as pls

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            show_time=True,
            markup=True,
            rich_tracebacks=True,
            tracebacks_suppress=[pl, pls, np],
        )
    ],
)
log = logging.getLogger(__name__)


def rank_to_pref(ranking):
    """Converts a ranking to a preference."""
    id_col_name = ranking.select(pls.by_index(0)).to_series().name
    preferences = ranking.select(
        [
            pl.col(id_col_name).sort_by(c).alias(c)
            for c in ranking.columns
            if c != id_col_name
        ]
    )
    return preferences


def pref_to_rank(preferences):
    """Converts a preference to a ranking."""
    o = preferences.select(
        pl.concat_list(preferences.columns).explode().unique().sort().alias("")
    )  # .with_row_index(offset=1)

    ranking = pl.concat(
        [
            o.join(
                preferences.with_row_index(offset=1),
                how="full",
                left_on="",
                right_on=c,
                maintain_order="left",
            ).select(pl.col("index").alias(c))
            for c in preferences.columns
        ],
        how="horizontal",
    )
    return pl.concat([o, ranking], how="horizontal")


""""
def ranking_matrix(A, B):
    T = pl.concat([A, B], how="horizontal")

    TT = T.with_columns(pl.concat_list(A.columns[0], B.columns[0]))
    for ab in zip(A.columns[1:], B.columns[1:]):
        TT = TT.with_columns(pl.concat_list(*ab))
    TTT = TT.select(pl.col(A.columns))

    return TTT.insert_column(0, pl.Series("names", B.columns))
"""


def check_valid_pref(preferences):
    """A valid set of preferences has all unique entries in each column, TODO"""
    repeats = preferences.select(
        (~pl.all_horizontal((pl.all().is_unique() | pl.all().is_null()).all())).alias(
            "repeats"
        )
    ).get_column("repeats")[0]
    return not repeats


def check_valid_rank(ranking):
    """A valid ranking has no ties, TODO"""
    ties = ranking.select(
        (~pl.all_horizontal((pl.all().is_unique() | pl.all().is_null()).all())).alias(
            "ties"
        )
    ).get_column("ties")[0]
    return not ties


def check_valid_match(match, applicants, reviewers):
    # TODO
    pass


def check_valid_assgn(assgn, applicants, reviewers):
    # TODO
    pass


def assgn_to_match(assgn):
    # TODO
    pass


def match_to_assgn(match):
    # TODO
    pass


def get_rank(ranking, ranker, ranked):
    idx = ranking.select(pl.arg_where(pl.col("") == ranked)).item()
    return ranking[ranker][idx]


def check_unstable(match, applicant_ranking, reviewer_ranking):
    applicants = applicant_ranking.columns[1:]  # assume unique applicants
    for a, b in it.permutations(applicants, 2):
        A = (
            match.select(c for c in match.iter_columns() if a in c).to_series().name
        )  # the reviewer a is matched to
        B = (
            match.select(c for c in match.iter_columns() if b in c).to_series().name
        )  # the reviewer b is matched to

        b_prefers_A = get_rank(applicant_ranking, b, A) < get_rank(
            applicant_ranking, b, B
        )
        A_prefers_b = get_rank(reviewer_ranking, A, b) < get_rank(
            reviewer_ranking, A, a
        )
        if b_prefers_A and A_prefers_b:
            return True
    # else
    return False


def check_stable(*args, **kwargs):
    return not check_unstable(*args, **kwargs)


from .brute import *
from .def_acc import *


def main() -> None:
    rich.print("Hello from [italic red]carousel[/italic red]!")


if __name__ == "__main__":
    main()

import polars as pl
from .def_acc import deferred_acceptance_GS


def check_match_unstable(
    match: pl.DataFrame,
    applicant_prefs: pl.DataFrame,
    position_prefs: pl.DataFrame,
    capacities: pl.DataFrame,
    *,
    app_col: str = "applicant",
    pos_col: str = "position",
    rank_col: str = "rank",
):
    """
    Check match stability between applicants and positions.

    parameters
    ---
    match: pl.DataFrame
    | applicant | position |

    applicant_prefs: pl.DataFrame
    | applicant | position | rank |

    position_prefs: pl.DataFrame
    | position | applicant | rank |

    """
    pass  # TODO


def check_match_stable(
    match: pl.DataFrame,
    applicant_prefs: pl.DataFrame,
    position_prefs: pl.DataFrame,
    capacities: pl.DataFrame,
    *,
    app_col: str = "applicant",
    pos_col: str = "position",
    rank_col: str = "rank",
) -> bool:
    """
    Check match stability between applicants and positions.

    parameters
    ---
    match: pl.DataFrame
    | applicant | position |

    applicant_prefs: pl.DataFrame
    | applicant | position | rank |

    position_prefs: pl.DataFrame
    | position | applicant | rank |

    """
    pass  # TODO


def pref_to_rank(
    p: pl.DataFrame, ranker_col: str, rankee_col: str, rank_col: str = "rank"
) -> pl.DataFrame:
    """
    Convert a preference list (long table) into a ranking (wide table).

    """
    return p.pivot(
        on=rankee_col, index=ranker_col, values=rank_col, aggregate_function="first"
    ).sort(ranker_col)


def rank_to_pref(
    r: pl.DataFrame,
    ranker_col: str,
    rankee_col: str,
    rank_col: str = "rank",
    rank_dtype=pl.UInt32,
) -> pl.DataFrame:
    """
    Convert a ranking (wide table) into a preference list (long table).

    """
    cols = [c for c in r.columns if c != ranker_col]

    return (
        r.unpivot(
            on=cols, index=ranker_col, variable_name=rankee_col, value_name=rank_col
        )
        .with_columns(pl.col(rank_col).cast(rank_dtype))
        .sort([ranker_col, rank_col])
    )


def default_convranks(
    prefs: pl.DataFrame, ranker_col: str, rankee_col: str, rank_col: str = "rank"
):
    """
    Default converse rankings -- uniform ranking/no preference.
    """
    rankees = [c for c in prefs.columns if c != ranker_col]

    rankers = prefs[ranker_col].to_list()

    return pl.DataFrame(
        {rankee_col: rankees, **{r: [1] * len(rankees) for r in rankers}}
    )


def default_caps(position_prefs: pl.DataFrame, pos_col: str = "position"):
    """
    Default capacities -- one of each.
    """
    positions = position_prefs[pos_col].to_list()
    return pl.DataFrame(
        {pos_col: positions, "capacity": [1 for _, _ in enumerate(positions)]}
    )


def def_acc_GS(
    applicant_prefs: pl.DataFrame,
    position_prefs: pl.DataFrame,
    capacities: pl.DataFrame,
    *,
    app_col: str = "applicant",
    pos_col: str = "position",
    rank_col: str = "rank",
    by: str = "ranking",  # alt: "preference"
) -> pl.DataFrame:
    """
    Find the Gale-Shapley deferred-acceptance proposer-optimal matching.
    """
    if by == "preference":
        return deferred_acceptance_GS(
            applicant_prefs,
            position_prefs,
            capacities,
            app_col=app_col,
            pos_col=pos_col,
            rank_col=rank_col,
        )
    elif by == "ranking":
        return deferred_acceptance_GS(
            rank_to_pref(applicant_prefs, app_col, pos_col, rank_col=rank_col),
            rank_to_pref(position_prefs, pos_col, app_col, rank_col=rank_col),
            capacities,
            app_col=app_col,
            pos_col=pos_col,
            rank_col=rank_col,
        )
    else:
        raise NotImplementedError(f"`def_acc_GS` with by={by} not implemented!")

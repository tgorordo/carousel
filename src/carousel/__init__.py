from .def_acc import *


def check_match_unstable(
    match,
    applicant_prefs,
    position_prefs,
    capacities,
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
    pass # TODO


def check_match_stable(
    match,
    applicant_prefs,
    position_prefs,
    capacities,
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
    pass # TODO
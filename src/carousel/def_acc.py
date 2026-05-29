from collections import deque
import heapq

import numpy as np
import polars as pl


def GS_deferred_acceptance(
    applicant_prefs: pl.DataFrame,
    position_prefs: pl.DataFrame,
    capacities: pl.DataFrame,
    *,
    app_col: str = "applicant",
    pos_col: str = "position",
    rank_col: str = "rank",
) -> pl.DataFrame:
    """
    Compute the proposer-optimal Gale-Shapley deferred acceptance stable matching for a
    college-admissions problem between "applicants" and "positions" with specified capacities.

    parameters
    ---
    applicant_prefs: pl.DataFrame
    A 3-column ranking of positions by applicants. | applicant | position | rank |
    (lower rank is more preferred).


    position_prefs: pl.DataFrame
    A 3-column ranking of applicants by positions. | position | applicant | rank |
    (lower rank is more preferred).

    capacities: pl.DataFrame
    A listing of position capacities. | position | capacity |

    returns
    ---
    matches: pl.DataFrame
    A two-column match between applicants and positions (e.g. students and colleges).
    | applicant | position |
    """

    app_idxs = (
        applicant_prefs.select(app_col).unique().sort(app_col).with_row_index("app_idx")
    )

    pos_idxs = (
        position_prefs.select(pos_col).unique().sort(pos_col).with_row_index("pos_idx")
    )

    n_apps = app_idxs.height
    n_poss = pos_idxs.height

    ap = (
        applicant_prefs.join(app_idxs, on=app_col)
        .join(pos_idxs, on=pos_col)
        .sort(["app_idx", rank_col])
    )
    al = (
        ap.group_by("app_idx", maintain_order=True)
        .agg(pl.col("pos_idx"))
        .sort("app_idx")
    )
    app_prefs = al["pos_idx"].to_list()

    max_pref_len = max((len(x) for x in app_prefs), default=0)

    pmat = np.full((n_apps, max_pref_len), -1, dtype=np.int32)
    for i, r in enumerate(app_prefs):
        pmat[i, : len(r)] = r

    pp = (
        position_prefs.join(app_idxs, on=app_col)
        .join(pos_idxs, on=pos_col)
        .sort(["pos_idx", rank_col])
    )
    worst_rank = np.iinfo(np.int32).max

    ranking = np.full((n_poss, n_apps), worst_rank, dtype=np.int32)
    for r in pp.iter_rows(named=True):
        ranking[r["pos_idx"], r["app_idx"]] = r[rank_col]

    caps = capacities.join(pos_idxs, on=pos_col).sort("pos_idx")
    cap = caps["capacity"].to_numpy().astype(np.int32)

    # ---

    next_c = np.zeros(n_apps, dtype=np.int32)
    matched_pos = np.full(n_apps, -1, dtype=np.int32)

    free = deque(np.arange(n_apps, dtype=np.int32))

    pos_heaps: list[list[tuple[int, int]]] = [[] for _ in range(n_poss)]

    while free:
        a = free.popleft()

        while next_c[a] < max_pref_len:
            p = pmat[a, next_c[a]]
            next_c[a] += 1

            if p == -1:
                break
            # else

            arank = ranking[p, a]

            if arank == worst_rank:
                continue

            heap = pos_heaps[p]

            if len(heap) < cap[p]:
                heapq.heappush(heap, (-arank, a))
                matched_pos[a] = a
                break

            worst_neg_rank, worst_app = heap[0]
            worst_rank_current = -worst_neg_rank

            if arank < worst_rank_current:
                heapq.heapreplace(heap, (-arank, a))
                matched_pos[a] = a
                matched_pos[worst_app] = -1

                free.append(worst_app)
                break

    matches = (
        pl.DataFrame({"app_idx": np.arange(n_apps), "pos_idx": matched_pos})
        .filter(pl.col("pos_idx") != -1)
        .join(app_idxs, on="app_idx")
        .join(pos_idxs, on="pos_idx")
        .select([app_col, pos_col])
        .sort(app_col)
    )

    return matches

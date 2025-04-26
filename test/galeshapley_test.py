import polars as pl
import polars.selectors as pls
import numpy as np

from polars.testing import assert_frame_equal

import pytest, rich
from hypothesis import given, strategies as st

import carousel as crsl

rng = np.random.default_rng()


@st.composite
def rankings(draw, names=["a", "b", "c"], choices=["A", "B", "C"]):
    h = pl.DataFrame({"": choices})
    r = pl.DataFrame(
        {n: draw(st.just(rng.permutation(len(choices)) + 1)) for n in names}
    )  # should add None option in generation of valid rankings
    return pl.concat([h, r], how="horizontal")


@st.composite
def preferences(draw, names=["a", "b", "c"], choices=["A", "B", "C"]):
    p = pl.DataFrame(
        {
            n: draw(st.just(rng.choice(choices, size=len(choices), replace=False)))
            for n in names
        }
    )
    return p


p = pl.DataFrame({"a": ["A", "C", "B"], "b": ["B", "A", "C"], "c": ["C", "B", "A"]})
r = pl.DataFrame({"": ["A", "B", "C"], "a": [1, 3, 2], "b": [2, 1, 3], "c": [3, 2, 1]})


def test_invalid_pref():
    pp = pl.DataFrame(
        {"a": ["A", "A", "B"], "b": ["B", "A", "C"], "c": ["C", "B", "A"]}
    )
    assert crsl.check_valid_pref(pp) is False


def test_pref_to_rank():
    assert_frame_equal(crsl.pref_to_rank(p), r, check_dtypes=False)


def test_invalid_rank():
    rr = pl.DataFrame(
        {"": ["A", "B", "C"], "a": [1, 1, 2], "b": [2, 1, 3], "c": [3, 2, 1]}
    )
    assert crsl.check_valid_pref(rr) is False


def test_rank_to_pref():
    assert_frame_equal(crsl.rank_to_pref(r), p, check_dtypes=False)


@given(rankings())
def test_valid_rank(R):
    assert crsl.check_valid_rank(R)


@given(rankings())
def test_ranks_tofrom_prefs(R):
    assert_frame_equal(crsl.pref_to_rank(crsl.rank_to_pref(R)), R, check_dtypes=False)


@given(preferences())
def test_valid_pref(P):
    assert crsl.check_valid_pref(P)


@given(preferences())
def test_prefs_tofrom_ranks(P):
    assert_frame_equal(crsl.rank_to_pref(crsl.pref_to_rank(P)), P, check_dtypes=False)


def test_eg2_unstable():
    ar = pl.DataFrame(
        {
            "": ["A", "B", "C", "D"],
            "a": [1, 2, 3, 4],
            "b": [1, 4, 3, 2],
            "c": [2, 1, 3, 4],
            "d": [4, 2, 3, 1],
        }
    )
    rr = pl.DataFrame(
        {
            "": ["a", "b", "c", "d"],
            "A": [3, 4, 2, 1],
            "B": [3, 1, 4, 2],
            "C": [2, 3, 4, 1],
            "D": [3, 2, 1, 4],
        }
    )
    match = pl.DataFrame({"A": ["a"], "B": ["b"], "C": ["c"], "D": ["d"]})

    assert crsl.check_unstable(match, ar, rr)


def test_eg2_isstable():
    ar = pl.DataFrame(
        {
            "": ["A", "B", "C", "D"],
            "a": [1, 2, 3, 4],
            "b": [1, 4, 3, 2],
            "c": [2, 1, 3, 4],
            "d": [4, 2, 3, 1],
        }
    )
    rr = pl.DataFrame(
        {
            "": ["a", "b", "c", "d"],
            "A": [3, 4, 2, 1],
            "B": [3, 1, 4, 2],
            "C": [2, 3, 4, 1],
            "D": [3, 2, 1, 4],
        }
    )
    match = pl.DataFrame({"A": ["c"], "B": ["d"], "C": ["a"], "D": ["b"]})

    assert crsl.check_stable(match, ar, rr)


@given(
    rankings(names=["a", "b", "c", "d"], choices=["A", "B", "C", "D"]),
    rankings(names=["A", "B", "C", "D"], choices=["a", "b", "c", "d"]),
)
def test_defacc_isstable(applicant_rankings, reviewer_rankings):
    match = crsl.deferred_acceptance(applicant_rankings, reviewer_rankings)
    assert crsl.check_stable(match, applicant_rankings, reviewer_rankings)

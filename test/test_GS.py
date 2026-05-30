import polars as pl
from polars.testing import assert_frame_equal
from carousel import def_acc_GS


def test_prefs():
    people_prefs = pl.DataFrame(
        {
            "people": [
                "Alice",
                "Alice",
                "Alice",
                "Bob",
                "Bob",
                "Bob",
                "Charlie",
                "Charlie",
                "Charlie",
            ],
            "fruit": [
                "apple",
                "banana",
                "cherry",
                "banana",
                "cherry",
                "apple",
                "cherry",
                "apple",
                "banana",
            ],
            "rank": [1, 2, 3, 1, 2, 3, 1, 2, 3],
        }
    )

    fruit_prefs = pl.DataFrame(
        {
            "fruit": [
                "apple",
                "apple",
                "apple",
                "banana",
                "banana",
                "banana",
                "cherry",
                "cherry",
                "cherry",
            ],
            "people": [
                "Alice",
                "Bob",
                "Charlie",
                "Alice",
                "Bob",
                "Charlie",
                "Alice",
                "Bob",
                "Charlie",
            ],
            "rank": [1, 1, 1, 1, 1, 1, 1, 1, 1],  # fruits have no preferences
        }
    )

    capacities = pl.DataFrame(
        {
            "fruit": ["apple", "cherry", "banana"],
            "capacity": [1, 1, 1],  # have one of each
        }
    )

    assert_frame_equal(
        def_acc_GS(
            people_prefs,
            fruit_prefs,
            capacities,
            app_col="people",
            pos_col="fruit",
            by="preference",
        ).sort(["people", "fruit"]),
        pl.DataFrame(
            {
                "people": ["Alice", "Bob", "Charlie"],
                "fruit": ["apple", "banana", "cherry"],
            }
        ).sort(["people", "fruit"]),
    )


def test_ranks():
    people_ranks = pl.DataFrame(
        {
            "people": ["Alice", "Bob", "Charlie"],
            "apple": [1, 3, 2],
            "banana": [2, 1, 3],
            "cherry": [3, 2, 1],
        }
    )

    fruit_ranks = pl.DataFrame(
        {
            "fruit": ["apple", "banana", "cherry"],
            "Alice": [1, 1, 1],
            "Bob": [1, 1, 1],
            "Charlie": [1, 1, 1],
        }
    )

    capacities = pl.DataFrame(
        {
            "fruit": ["apple", "cherry", "banana"],
            "capacity": [1, 1, 1],  # have one of each
        }
    )

    assert_frame_equal(
        def_acc_GS(
            people_ranks,
            fruit_ranks,
            capacities,
            app_col="people",
            pos_col="fruit",
            by="ranking",
        ).sort(["people", "fruit"]),
        pl.DataFrame(
            {
                "people": ["Alice", "Bob", "Charlie"],
                "fruit": ["apple", "banana", "cherry"],
            }
        ).sort(["people", "fruit"]),
    )

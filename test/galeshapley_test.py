import polars as pl
from polars.testing import assert_frame_equal
from carousel import GS_deferred_acceptance


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
        GS_deferred_acceptance(
            people_prefs, fruit_prefs, capacities, app_col="people", pos_col="fruit"
        ).sort(["people", "fruit"]),
        pl.DataFrame(
            {
                "people": ["Alice", "Bob", "Charlie"],
                "fruit": ["apple", "banana", "cherry"],
            }
        ).sort(["people", "fruit"]),
    )

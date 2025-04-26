def deferred_acceptance(applicant_rankings, reviewer_rankings):
    """Find Gale-Shapley deferred-acceptance stable matchings for preferences A, R."""
    reviewer_rankings = reviewer_rankings.rename(
        {reviewer_rankings.columns[0]: "applicant"}
    )

    app_prefs = rank_to_pref(applicant_rankings)
    offers = app_prefs.transpose(
        include_header=True,
        header_name="applicant",
        column_names=["pref" + str(i + 1) for i in range(app_prefs.width)],
    ).with_columns(pl.coalesce(pl.all().exclude("applicant")).alias("offer"))

    # offers = pl.concat(pl.align_frames(offers, reviewer_rankings, on="applicant"), how="horizontal")
    offers = pl.concat([offers, reviewer_rankings], how="align_left")

    match = pl.DataFrame(
        {
            r: offers.select(pl.col("applicant", "offer").sort_by(r))
            .select(
                pl.when(pl.col("offer").eq(r)).then(pl.col("applicant")).otherwise(None)
            )
            .select(pl.all().fill_null(strategy="backward").first())
            .to_series()
            for r in reviewer_rankings.columns[1:]
        }
    )  # .select(pl.all().fill_null(strategy="backward").first())

    # while check_unstable(match, applicant_rankings, reviewer_rankings):
    while match.select(pl.any_horizontal(pl.all().has_nulls())).item():
        # TODO null applicant preferences that rejected

        rejected_applicants = offers.select(
            pl.col("applicant").is_in(match.row(0)).alias("matched")
        )

        return match

        offers = offers.with_columns(pl.col("pref"))

        offers = offers.with_columns(
            pl.coalesce(
                # TODO: select prefn columns using a regex
            ).alias("offer")
        )

        # TODO update match

    # else if stable
    return match

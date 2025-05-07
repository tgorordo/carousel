import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Caltech Hovse Rotation Example""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Imports""")
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl, polars.selectors as pls
    import numpy as np, faker as fk
    import carousel as crsl
    return crsl, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Generating Rotation Rankings""")
    return


@app.cell
def _(crsl, pl):
    ar = pl.DataFrame({ "": ["A", "B", "C", "D"], "a": [1, 2, 3, 4], "b": [1, 4, 3, 2], "c": [2, 1, 3, 4], "d": [4, 2, 3, 1]})
    rr = pl.DataFrame({ "": ["a", "b", "c", "d"], "A": [3, 4, 2, 1], "B": [3, 1, 4, 2], "C": [2, 3, 4, 1], "D": [3, 2, 1, 4]})
    m = pl.DataFrame({"A": ["c"], "B": ["d"], "C": ["a"], "D": ["b"]})
    crsl.check_stable(m, ar, rr)
    return


@app.cell
def _():
    hovses = ["Blacker", "Dabney", "Ricketts", "Fleming", "Page", "Lloyd", "Venerable", "Avery"]
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

---
bibliography: REFERENCES.bib
...

# Carousel
*A simple Stable Matching Solver.*

`carousel` is a solver for the 
[Envy-free](https://en.wikipedia.org/wiki/Envy-free_matching)
[Stable matching problem](https://en.wikipedia.org/wiki/Stable_marriage_problem) based on some naive modifications to the 
[Gale-Shapley Algorithm](https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm), written in Python.

## Algorithms

### Gale-Shapley Deferred Acceptance

The most basic version(s) of the stable matching problem was outlined and solved in [@gale&shapley1962] and won Shapley the 
[2012 Nobel Prize in Economics](https://www.nobelprize.org/prizes/economic-sciences/2012/popular-information/).

The basic problem being solved is as follows:

#### Stable Marriage Problem
The "Stable Marriage problem" TODO

TODO

#### College Admissions Problem 
Solving the stable marriage problem also provides a solution to the "College Admissions Problem", 
with just a little more work.

TODO

## Data - Input/Output
All [input table formats supported by `polars`](https://docs.pola.rs/user-guide/io/) are supported by `carousel` (`csv`, `excel`, `json` to name a few), 
which accepts a few inter-related tabular schemes for the input/output data.

### Input
Input describes the preferences/rankings of the "applicants" of "reviewers" to which they will be matched (possibly many-to-one, as in the "College Admission Problem"),
as well as the preferences/rankings for the reviwers of applicants.
Input should be in one of three forms:

#### Preferences
Preferences enumerate by-name some preferences in descending order, 
e.g. the fruit preferences of Alice, Bob and Charlie are:

| Alice  | Bob    | Charlie |
|--------|--------|---------|
| apple  | banana | cherry  |
| cherry | apple  | banana  |
| banana | cherry | apple   |

where for e.g. Alice prefers apples to cherries (so they appear higher in her preferences).

#### Rankings
Rankings are like preferences, but are numerically ordered against a list of things;
e.g. Alice, Bob and Charlie rank the fruit apples, bananas and cherries as:

| fruit  | Alice | Bob | Charlie |
|--------|-------|-----|---------|
| apple  |   1   |  2  |    3    |
| banana |   3   |  1  |    2    |
| cherry |   2   |  3  |    1    |

#### Ranking Matrix
In order to perform a matching, `carousel` either needs a pair of preferences
(e.g. a set of doctor's preferences for residencies, and a set of residencies' preferences for doctors),
a pair of corresponding rankings, *or* a matrix encoding both rankings at once:

| names   | Alice      | Bob     | Charlie   |
|---------|------------|---------|-----------|
| Baylor  |   (1, 3)   |  (2, 2) |   (3, 1)  |
| CaseMed |   (3, 2)   |  (1, 1) |   (2, 3)  |
| Emory   |   (2, 1)   |  (3, 3) |   (1, 2)  |

### Output

#### Matching
A matching is a table whose rows list the applicants matched to each reviewer
e.g. a matching from the med-school ranking matrix in the previous section might look like

| Baylor | CaseMed | Emory   |
|--------|---------|---------|
| Alice  | Bob     | Charlie |
| `None` | Daina   | `None`  |

#### Assignments
An assignment is a table whose row lists which reviewer each applicant was matched to.
e.g.

| Alice  | Bob     | Charlie | Daina   |
|--------|---------|---------|---------|
| Baylor | CaseMed | Emory   | CaseMed |

TODO check/make stable.

TODO matching more people per school e.g.




## Usage

There are 4 main ways to use Carousel:

### UO Pages Server - CGI Form
An HTML form submission interface is hosted at

> [`https://pages.uoregon.edu/tgorordo/forms/carousel.html`](https://pages.uoregon.edu/tgorordo/forms/carousel.html)

using the [pages.uoregon.edu CGI feature](https://service.uoregon.edu/TDClient/2030/Portal/KB/ArticleDet?ID=43069).

Submit your applicant and reviewer preferences in tabular form,
or as excel uploads and the server will return a table of matches for you to choose from.

### Command Line Binary

TODO

### GUI Binary

TODO

### Python Library/Development
If you prefer to invoke `carousel` directly (or incorporate it as a library into another script)
in a python environment instead of using any of the bundled/released versions of the program described above (or wish to
reproduce those bundles), you can do so using the [`uv` environment/package/project manager](https://github.com/astral-sh/uv)
or a raw python virtual environment using the [`venv` module](https://docs.python.org/3/library/venv.html)
(if you need an intro to python `venv`s see [this page](https://pages.uoregon.edu/tgorordo/uoph410-510a_Image-Analysis/venvs.html)).

Some extra command-line development conveniences are available if you use the tools:  

- [`just`](https://github.com/casey/just) is a taskrunner that can execute the provided `justfile` of some common useful commands.
- [`direnv`](https://github.com/direnv/direnv) with [`nix` (shell)](https://github.com/NixOS/nix) can guarantee minimal development tooling without polluting your broader environment. i.e. they can auto-install and run all of carousel's tooling in an environment specific to your development directory.

but everything provided by these tools can also be done using more standard/default shell tooling. 
[`uv`](https://github.com/astral-sh/uv) as your package/environment manager is highly recommended, however.

TODO

## Post-Selection
It's often desirable to enforce additional criteria on solutions 
that are not well-posed within the core optimization problem.
Since the solver itself is stochastic to some extent, these are often most easily implemented 
by a post-selection.


## Examples
Here are some usage examples:

### Departmental TA Assignments
TODO

### Caltech Housing Rotation
TODO

## References
*See [`REFERENCES.bib`](REFERENCES.bib)*

[1]: 

TODO

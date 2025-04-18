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

The most basic versions of the stable matching problem was outlined and solved by [@gale&shapley1962]. 

TODO

## Usage
Using `carousel` is pretty simple once it's set up: given some input rankings, and some post-selection criteria 
the program should generate a landscape of valid matching solutions for you to choose from (and can generate more on request).

### Installation, Setup, Dependencies & Tooling
There are a number of ways to guarantee you have the required dependencies to run `carousel`.
The most complete method is using `uv` (with `nix` and `direnv`), but a plain/more barebones setup using `venv` is also possible.

#### Setup and run with `uv`
`carousel` was developed using the the [`uv`](https://github.com/astral-sh/uv) package and project manager.

TODO

#### Raw setup with `venv`
It's possible to only use only default Python tooling, if so desired, via the 
[`venv` module](https://docs.python.org/3/library/venv.html).

TODO

#### Convenience `direnv` and `nix` environment management.
TODO

### Matching: Input & Output

All [input table formats supported by `polars`](https://docs.pola.rs/user-guide/io/) are supported by `carousel`.
Input data should be in one of three forms:

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

### Matching: Post-Selection
It's often desirable to enforce additional criteria on solutions 
that are not well-posed within the core optimization problem.
Since the solver itself is stochastic, these are often most easily implemented 
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

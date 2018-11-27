# pyjanitor: A Cleaner API for Cleaning Data

## Authors

- Eric J Ma

## Abstract

The `pandas` library has become the de facto library for data wrangling in the Python programming language. However, inconsistencies in the `pandas` application programming interface (API), while idiomatic due to historical use, prevent use of expressive, fluent programming idioms that enable self-documenting `pandas` code. Here, I introduce `pyjanitor`, an open source Python package that provides an API layer on top of the `pandas` API. `pyjanitor` makes heavy use of method chaining, prioritizing verbs as method names and arguments in the same style as the R package `dplyr`. This provides consistency in the API design, while also matching idioms that end-users would be accustomed to. Here, I also show a side-by-side comparison of code to accomplish the same data processing
tasks, and outline generalizable principles for data processing API design.

## Introduction

In a data-oriented age, data preprocessing is an unavoidable task. Data wrangling is thought to occupy 80% of a data scientist’s time [^datacleaning]. There are multiple avenues to make this 80% of time more efficiently spent, such as providing proper schema and metadata documentation on data stores, providing data scientists with cleaned data, and providing high performance compute for data processing. An avenue possibly less explored is the ease-of-use of tooling in the hands of a data scientist.

[^datacleaning]: https://www.nytimes.com/2014/08/18/technology/for-big-data-scientists-hurdle-to-insights-is-janitor-work.html

Python, a high-level programming language designed for ease of use, is one of the two most popular data science languages, the other being the R statistical language [^R]. The breadth of tools available in both languages, and the development of interoperability packages (rpy2 [^rpy2], reticulate [^reticulate]), reflect the popularity of high-level, easy-to-use languages for wrangling data. Within the PyData stack, `pandas` is the *de facto* tool for data manipulation in the Python programming language. As reflected by the eye-catching and pun-laden title, “Pandas responsible for Python explosion” [^explosion], without `pandas` and the rest of the PyData stack, the Python programming language probably would have remained a hobbyist, scripting-oriented language. (By no means does my previous comment diminish the role of the other packages in the ecosystem; individual elements in a strong ecosystem play well with one another, and the PyData ecosystem is a strong and vibrant one.)

[^R]: https://www.r-project.org/
[^rpy2]: https://rpy2.readthedocs.io/en/version_2.8.x/
[^reticulate]: https://rstudio.github.io/reticulate/
[^explosion]: https://www.theregister.co.uk/2017/09/14/python_explosion_blamed_on_pandas/


## Wishlist: An Extensible and Fluent Interface for Data Processing

That explosion of Python was measured by a StackOverflow data science study. While by no means a rigorously structured observational study (#double-check), the StackOverflow article does reflect the popularity of `pandas`, as a high number of questions being asked about a tool is generally reflective of a high number of users using that tool. However, popularity on StackOverflow may also be indicative of a latent issue: the high number of questions asked about how to accomplish a task with `pandas` may be indicative of the `pandas` API being targeted at a lower-level than what a data scientist is intuiting. By no means should we blame the `pandas` developers for this; rather, this is something to be celebrated, because it means that the building blocks for more intuitive abstractions are in place.

A case in point is the following elementary set of data preprocessing operations

1. Standardizing column names to snake-case (spelled\_like\_this, rather than Spelled Like This).
2. Removing unnecessary columns.
3. Adding a column of data.
4. Transforming a column through a function.

To do this with the `pandas` API, one might write the following code.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame(...)
# standardize column names.
df.columns =[i.lower().replace(' ', '_') for i in df.columns]
# remove unnecessary columns
del df['column_name_14']
# transform a column by taking the log
df['column_name_13'] = df['column_name_13'].apply(np.log10)
```

Through many years of popularity, this coding style has become established as being idiomatic. However, this is also a non-fluent expression of what is being accomplished, which hampers readability,
and hence maintainability. In terms of API design, we might want a block of code that reads as follows:

```python
import pandas as pd
import numpy as np
import janitor

df = (
    pd.DataFrame(...)
    .clean_names()
    .remove_column('column_name_14')
    .transform('column_name_13', np.log10)
)
```

This is the API design that `pyjanitor` aims to provide to `pandas` users. By using a fluent API design, `pyjanitor` explicitly targets a `pandas`-compatible API that empowers data scientists to
express their data processing code using an expressive, domain-specific-language-like (DSL-like) code.

## `pyjanitor`: History, Design, and Architecture

### History of `pyjanitor`

`pyjanitor` started as a Python port of the R package `janitor`, which is a data cleaning package for R users. The initial goal was to explicitly copy the `janitor` function names while engineering it to be compatible with `pandas` DataFrames, following Pythonic idioms, such as the method chaining provided by `pandas`. As the project evolved, the scope broadened, to provide a defined and expressive DSL for data processing, centered around the DataFrame object as a first-class citizen. In addition, “reverse ports” [^backport] from `pyjanitor` back to `janitor` are strongly encouraged, to encourage sharing of good ideas that get developed across language barriers.

[^backport]: I am hesitant to call this a back port, because that would imply that `janitor` is an outdated tool. By no means is this so. Hence, a “reverse” port appears to be the most appropriate
replacement name.


### Architecture

`pyjanitor` relies entirely on the `pandas` extension API, which allows developers to create functions that behave as if they were native `pandas` DataFrame class methods. The only requirement here is that the first argument to any function be a `pandas` DataFrame object:

```python
def data_cleaning_function(df, **kwargs):
    ...
    # data cleaning functions go here
    ...
    return df
```

In order to reduce the amount of boilerplate required, `pyjanitor` also makes heavy use of `pandas_flavor`, which provides an easy-to-use function decorator that handles class method registration. As such, to extend the `pandas` API with more class-method-like functions, we just have to decorate the custom function as follows:

```python
import pandas_flavor as pf
@pf.register_dataframe_method
def data_cleaning_function(df, **kwargs):
    ...
    # data cleaning functions go here
    ...
    return df
```

Underneath each data cleaning function, we use lower-level `pandas` syntax. As such, each data cleaning function is nothing more than an intuitive convenience wrapper around canonical `pandas` syntax.

### Design

`pyjanitor` functions are named with verb expressions. This helps achieve the DSL-like nature of the API. Hence, if I want to “clean names”, the end user can call on the `.clean_names()` function; if the end user wants to “remove all empty rows and columns, they can call on `.remove_empty()`. As far as possible, function names are expressed using simple English verbs that are understandable
cross-culturally, to ensure that this API is inclusive and accessible to the widest subset of users possible.

Likewise, keyword arguments are also named with verb expressions. For example, if one wants to preserve and record the original column names before cleaning, one can add the `preserve_original` keyword argument to the `.clean_names` method:

```python
df.clean_names(preserve_original=True, remove_special=True, ...)
```

As show in the code block example above, other keyword arguments that have been contributed to the function library can also be called on.

### Documentation and Development

API Documentation for `pyjanitor` is available on ReadTheDocs, at [https://pyjanitor.readthedocs.io/](https://pyjanitor.readthedocs.io/ "https://pyjanitor.readthedocs.io/").

Additionally, development takes place on GitHub, at: [https://github.com/ericmjl/pyjanitor](https://github.com/ericmjl/pyjanitor "https://github.com/ericmjl/pyjanitor").

The reception to `pyjanitor` has been encouraging thus far. Newcomer contributors to open source have made their maiden contributions to `pyjanitor`, and experienced software engineers have also chipped in. More significant has been the contributions from data scientists seeking a cleaner API for cleaning data. There is a salient lesson here: with open source tools, savvy users can help steer
development in a direction that they need.

As with most open source software development, maintenance and new feature development are entirely volunteer driven. Users are invited to post feature requests on the source repository issue tracker, but are more so invited to contribute an implementation themselves to share.

### Contributing

New contributions are always welcome. The process for contributing is documented on the source repository. At a high level, the main things to remember are to:

1. Consider first whether the proposed feature simplifies workflow tasks for `pandas` users, and whether there are native method-chainable `pandas` alternatives;
2. Use action phrases, where possible, for function names and keyword arguments;
3. Write a sufficiently descriptive docstring, and provide an API usage example;
4. Add test cases to the test suite.

For domain-specific functions, we recommend that users either:

1. Follow the programming idioms laid out in `pyjanitor` to build their own packages, or
2. Make a contribution to an appropriate sub-namespace in pyjanitor, e.g. `pyjanitor.finance` or `pyjanitor.chemistry`, with a view towards breaking out the sub-namespace into its own package when matured.

## Comparison to other tools

**`janitor`**: This is the original source of inspiration for `pyjanitor`, and the original creator of `janitor` is aware of `pyjanitor`’s existence. A number of function names in `janitor` have been directly copied over to `pyjanitor` and re-implemented in a `pandas`-compatible syntax. R-janitor can be found at [https://github.com/sfirke/janitor](https://github.com/sfirke/janitor)

**`dplyr`**: The `dplyr` R package can be considered as “the originator” for verb-based data processing syntax. `janitor` extends `dplyr`. It is available for use by Python users through `rpy2`; however, its primary usage audience is R users.

**`pandas-ply`**: This is a tool developed by Coursera, and aims to provide the `dplyr`syntax to `pandas` users. One advantage that it has over `pyjanitor` is that symbolic expressions can be used inside functions, which automatically get parsed into an appropriate lambda function in Python.  However, the number of verbs available is restricted to the `dplyr` set. As of 24 November 2018, development was last seen 3 years ago. `pandas-ply` can be found at[https://github.com/coursera/pandas-ply](https://github.com/coursera/pandas-ply)

**`dplython`**:  Analogous to `pandas-ply`, `dplython` also aims to provide the `dplyr` syntax to `pandas` users. Development was last seen 2 years ago. `dplython` can be found at [https://github.com/dodger487/dplython](https://github.com/dodger487/dplython)

## Limitations of `pyjanitor`

At this moment, the most glaring limitation of `pyjanitor` is the inability to evaluate symbolic expressions. Doing so would greatly enable the filtering syntax. At the moment, to filter a dataframe by some column’s values requires two steps:

```python
df = pd.DataFrame(...)
df = df.filter_on((df['value_column'] < 3) & (df['value_column'] > 1))
```

With symbolic evaluation, we would be able to write something like:

```python
df = (
    pd.DataFrame(...)
    .filter(1 < X.value_column)
    .filter(X.value_column > 3)
)
```

The latter, which is possible (in a slightly different form) using pandas-ply (#double-check), is currently impossible with `pyjanitor`.

Apart from that, a minor technical limitation of `pyjanitor` is that it is still feature-incomplete. I anticipate that future maturation of `pyjanitor` through contributions from myself and the rest of the data science community will enable us to extend `pyjanitor`’s usage and scope, while remaining true to it being a general-purpose (and not domain-specific) data cleaning tool.

## Extensions beyond `pyjanitor`

`pyjanitor` does not aim to be the all-purpose data cleaning tool for all subject domains. Apart from providing generally useful data manipulation and cleaning routines, one can also think of it as a catalyst project for other specific domain applications. Following the verb-based grammar, one can imagine even more specific domain terms.

For example, one may imagine the creation of chemistry-oriented names, such as:
- `smiles2mol(df, col_name)`: to convert a column of smiles into RDKit [^rdkit] mol objects.
- `mol2graph(df, col_name)`: to convert a column of mol objects into graph objects.

[^rdkit]: https://www.rdkit.org/

Alternatively, one might imagine biology-oriented functions for commonly-used tasks, such as:
- `to_fasta(df, col_name, file_name)`: exporting a column of sequences to a FASTA file
- `compute_length(df, col_name, length_colname)`: to compute the length of a column of sequences.

The general idea of calling on verb-based function names that method chain in a *fluent* fashion can be applied in multiple domains. `pyjanitor` is by no means the first application; it is my hope that this article inspires others to develop domain-specific tools using the same ideas.

## Acknowledgments

I would like to thank the users who have made contributions to `pyjanitor`. These contributions have included documentation enhancements, bug fixes, development of tests, new functions, and new keyword arguments for functions. The list of contributors, which I anticipate will grow over time, can be found under `AUTHORS.rst` in the development repository.

I would also like to acknowledge Dr. Zachary Sailer, who developed `pandas-flavor`.


---
title: 'pyjanitor: Clean APIs for cleaning data'
tags:
  - Python
  - data science
  - data engineering
  - application programming interfaces
authors:
  - name: Eli S. Goldberg
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Eric J. Ma
    orcid: 0000-0003-0872-7098
    affiliation: 1
  - name: Zachary Barry
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Sam Zuckerman
    orcid: 0000-0000-0000-0000
    affiliation: 2
  - name: Zachary Sailer
    orcid: 0000-0000-0000-0000
    affiliation: 3
affiliations:
 - name: Novartis Institutes for Biomedical Resaerch
   index: 1
 - name: Institution 2
   index: 2
 - name: Project Jupyter
   index: 3
date: 9 March 2019
bibliography: references.bib
---

# Summary

The `pandas` library has become the de facto library for data wrangling in the Python programming language. However, inconsistencies in the `pandas` application programming interface (API), while idiomatic due to historical use, prevent use of expressive, fluent programming idioms that enable self-documenting `pandas` code. Here, we introduce `pyjanitor`, an open source Python package that provides a fluent API layer on top of the pandas API, enabling data scientists and engineers to write readable, self-documenting and maintainable code.

`pyjanitor` started originally as a Python port of the R package. However, as the project evolved, we recognized that a fluent API through method chaining when doing data preparation work could enhance the readability of code. We believe the following example adequately expresses why `pyjanitor` is a usability and code maintainability improvement over native `pandas` syntax. To perform a three-step data cleaning routine involving cleaning column names, transforming a column, and selecting a subset of columns, with `pyjanitor`, one would write:

```python
import pandas as pd
import numpy as np

df = (
    pd.DataFrame(...)
    .clean_names()
    .transform_column('readout', np.log10, 'readout_log10')
    .select_columns(['id', 'readout'])
)
```

This stands in contrast to original `pandas` syntax:

```python
import pandas as pd
import numpy as np
from pyjanitor import clean_names

df = pd.DataFrame()
df.columns = [clean_names(x) for x in df.columns]
df['readout_log10'] = np.log10(df['readout'])
df = df[['id', 'readout']]
```

In addition to being designed for a fluent interface, domain-specific modules with optional dependencies are also available. For example, `pyjanitor` is used by EM for cheminformatics modelling work at NIBR, and has a number of convenience routines for generating RDKit in silico molecule objects and chemical fingerprints. Biology- and finance-oriented submodules are also under development.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

# Figures

Figures can be included like this: ![Example figure.](figure.png)

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References

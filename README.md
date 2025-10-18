<center>
    <img src="https://github.com/Ackrome/matplobblib/blob/master/image/notes/icon.svg" alt="icon" width="400" />
</center>

# matplobblib

[![PyPI Downloads](https://img.shields.io/pypi/dm/matplobblib.svg?label=PyPI%20downloads)](
https://pypi.org/project/matplobblib/)<br>
[![PyPI version](https://badge.fury.io/py/matplobblib.svg)](https://badge.fury.io/py/matplobblib)<br>
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)<br>
[![Python Version](https://img.shields.io/pypi/pyversions/matplobblib.svg)](https://pypi.org/project/matplobblib/)<br>

## Choose language:

- [English README](README.md) 🇬🇧
- [Русский README](README-ru.md) 🇷🇺

## Introduction

The `matplobblib` library provides a set of tools and functions for various subject areas, including Analysis and Data Structures (AISD), Probability Theory and Mathematical Statistics (TViMS), Machine Learning (ML), and Numerical Methods (NM).

## Table of Contents

- Installation
- Quick Start
- Modules
- Dependencies
- Contributing
- License
- Contacts

## Installation

To install the `matplobblib` library, execute the following command:

```bash
pip install matplobblib
```

Ensure you have Python version 3.6 or higher installed.

## Quick Start

Import the necessary modules and start using the functions:

```python
# Example of importing modules
import matplobblib.aisd as aisd
import matplobblib.tvims as tvims
import matplobblib.ml as ml
import matplobblib.nm as nm

# Example of using a function from the tvims module to display available topics
tvims.description()

# For detailed information about the functions of each module,
# refer to the respective README files of the modules.
```

## Modules

The library includes the following main modules:

* ### **[aisd](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/aisd)**: Implementations of various algorithms and data structures.
* ### **[tvims](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/tvims#readme)**: Functions and tools for probability theory and mathematical statistics. Includes theoretical materials, calculations for random variables, hypothesis testing, and much more.
* ### **[ml](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/ml#readme)**: Tools and algorithms for machine learning tasks.
* ### **[nm](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm#readme)**:  Implementations of numerical methods for solving mathematical problems.

Each module has its own `README.md` with a more detailed description of its content and usage examples.

## Dependencies

Main project dependencies:

* numpy
* sympy
* pandas
* scipy
* pyperclip
* pymupdf
* graphviz
* statsmodels
* cvxopt

A complete list of dependencies can be found in the `setup.py` file.

## Contributing

We welcome contributions to the project! If you want to suggest improvements, fix bugs, or add new features, please create an Issue/Pull Request in the repository.

## License

The project is distributed under the MIT license. See the [LICENSE.txt](https://github.com/Ackrome/matplobblib/blob/master/LICENSE.txt) file for more details.

## Contacts

* **Author:** Ackrome
* **Email:** ivansergeyevicht@gmail.com
* **GitHub:** https://github.com/Ackrome/matplobblib

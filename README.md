# Handy Python

[![Test](https://github.com/leven-cn/handy.py/actions/workflows/test.yml/badge.svg)](https://github.com/leven-cn/handy.py/actions/workflows/test.yml)
[![Lint](https://github.com/leven-cn/handy.py/actions/workflows/lint.yml/badge.svg)](https://github.com/leven-cn/handy.py/actions/workflows/lint.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Collection of handy utils for Python.

## Usage

```bash
pip install handy-utils
```

```python
from handy_utils import xxx
```

## Features

- RE pattern of Chinese characters
- Find Chinese characters in a string
- RE pattern of domain name (English, Chinese)
- Domain name validation (English, Chinese)
- RE pattern of license plate (Chinese mainland, Hongkong)
- License plate validation (Chinese mainland, Hongkong)
- RE pattern of WeChat (Wexin) ID
- WeChat (Wexin) ID validation

## Scripts

### Run a GUI (based on Tcl/Tk) for RE (regular expression)

```bash
python -m handy_utils.re_tk
```

## License

[Apache License 2.0](https://github.com/leven-cn/handy.py/blob/master/LICENSE)

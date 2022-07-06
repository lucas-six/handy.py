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

- MapReduce on local host
- Decorators
  - **`@attrs`**: Add attributes to a function/method.
  - **`@accepts`** and **`@returns`**: Enforce function argument and return types.
  - **`@singleton`**: Define a class with a singleton instance.
- Regex patterns
  - Regex pattern of Chinese characters
  - Find Chinese characters in a string
  - Regex pattern of float numbers
  - Float number validation
  - Regex pattern of IPv4 addresses
  - IPv4 address validation
  - Regex pattern of email addresses
  - Email address validation
  - Regex pattern of HTML elements or tags
  - HTML element or tag validation
  - Regex pattern of domain names (English, Chinese)
  - Domain name validation (English, Chinese)
  - Regex pattern of color RGB hex
  - Color RGB hex validation
  - Password strength validation
  - Regex pattern of license plate (Chinese mainland, Hongkong)
  - License plate validation (Chinese mainland, Hongkong)
  - Regex pattern of WeChat (Wexin) ID
  - WeChat (Wexin) ID validation
  - Regex pattern of QQ number (ID)
  - QQ number (ID) validation
  - Regex pattern of Chinese telephone number
  - Chinese telephone number validation
  - Regex pattern of Chinese ID number
  - Chinese ID number validation

## Scripts

### Run a GUI (based on Tcl/Tk) for RE (regular expression)

```bash
python -m handy_utils.re_tk
```

## License

[Apache License 2.0](https://github.com/leven-cn/handy.py/blob/master/LICENSE)

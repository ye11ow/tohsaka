# Project Tohsaka

## Status
[![Build Status](https://travis-ci.org/ye11ow/tohsaka.svg?branch=master)](https://travis-ci.org/ye11ow/tohsaka)
[![Coverage Status](https://coveralls.io/repos/github/ye11ow/tohsaka/badge.svg?branch=master)](https://coveralls.io/github/ye11ow/tohsaka?branch=master)

## Test

```
# Unit test
python -m pytest tests/unit --cov=tohsaka --cov-report html --cov-report term

# E2E test
export OPENWEATHER_TOKEN=<TOKEN>
python -m pytest tests/mystic
```

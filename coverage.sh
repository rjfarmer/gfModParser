#!/usr/bin/bash

export PYTEST_COVERAGE=1
python -m pytest --cov=gfModParser --cov-report html 
xdg-open htmlcov/index.html

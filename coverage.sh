#!/usr/bin/bash

python -m pytest --cov=gfModParser --cov-report html
xdg-open htmlcov/index.html

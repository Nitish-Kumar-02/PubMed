# PubMed Fetcher

This project fetches research papers from PubMed based on a user query, identifies non-academic authors, and saves the results to a CSV file.

## Installation
```sh
pip install poetry  # Install Poetry
poetry install  # Install dependencies
```

## Usage
```sh
poetry run get-papers-list "cancer treatment" -f results.csv
```

# .gitignore
__pycache__/
*.pyc
*.pyo
.env

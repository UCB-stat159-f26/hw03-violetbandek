
# Tennis Career Match Visualization

This project is a Python package developed for STAT 159 at UC Berkeley. It retrieves professional tennis match data from Tennis Abstract and visualizes match outcomes based on player age and age differences between opponents.

## Installation

Install the package directly from GitHub:

```bash
python -m pip install "git+https://github.com/UCB-stat159-f26/hw03-violetbandek.git"
```

## Features

- Download professional tennis career match data.
- Process match dates, results, and opponent information.
- Calculate player ages and age differences.
- Visualize wins and losses using scatter plots.
- Support Serena Williams, Rafael Nadal, and additional players when their data and birthdates are available.

## Usage

```python
from tennis_career import get_player_matches, plot_player_matches
import matplotlib.pyplot as plt

# Serena Williams
serena = get_player_matches("Serena Williams")
fig = plot_player_matches(serena, "Serena Williams")
plt.show()

# Rafael Nadal
nadal = get_player_matches("Rafael Nadal")
fig = plot_player_matches(nadal, "Rafael Nadal")
plt.show()
```

## Testing

Run the tests from the repository's root directory:

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest tests/ -v
```

The tests check plotting functionality, missing columns, invalid player names, and female and male match data processing.

## Project Structure

- `src/tennis_career/data.py`: Downloads and processes match data.
- `src/tennis_career/plotting.py`: Creates match visualizations.
- `src/tennis_career/__init__.py`: Exposes public package functions.
- `tests/test_data.py`: Contains automated tests.
- `pyproject.toml`: Defines package metadata and dependencies.

## Data Source

Tennis Abstract: https://www.tennisabstract.com/

## Author

Violet Bandek  
University of California, Berkeley  
STAT 159 — Fall 2026
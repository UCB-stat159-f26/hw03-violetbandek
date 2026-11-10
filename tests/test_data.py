
import pandas as pd
import pytest

from tennis_career.data import get_player_matches
from tennis_career.plotting import plot_player_matches


def test_plot_returns_figure():
    """Plotting should return a Matplotlib figure."""
    matches = pd.DataFrame({
        "result": ["W", "L"],
        "player_age": [20, 21],
        "age_difference": [-2, 3],
    })
    fig = plot_player_matches(matches, "Test Player")
    assert len(fig.axes) == 1


def test_plot_missing_columns():
    """Missing required columns should raise an error."""
    with pytest.raises(ValueError, match="Missing columns"):
        plot_player_matches(pd.DataFrame())


def test_unknown_player():
    """An unsupported player should raise a meaningful error."""
    with pytest.raises(ValueError, match="Unknown player"):
        get_player_matches("Gaston Sanchez")

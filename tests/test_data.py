
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

from tennis_career.data import (
    _parse_matches,
    _clean_matches,
    _calculate_ages,
)


def test_female_player_data():
    """Female player data contains opponent birthdates."""
    row = [""] * 27
    row[0] = "19951030"
    row[1] = "Canadian Open"
    row[2] = "Carpet"
    row[4] = "L"
    row[11] = "Anne Miller"
    row[16] = "19770119"

    raw = "var morematchmx = " + repr([row]) + ";"
    matches = _clean_matches(_parse_matches(raw))
    result = _calculate_ages(matches, "1981-09-26")

    assert len(result) == 1
    assert result.iloc[0]["opponent"] == "Anne Miller"
    assert 18 < result.iloc[0]["opponent_age"] < 19


def test_male_player_data():
    """Male player data contains numeric opponent ages."""
    row = [""] * 49
    row[0] = "20010910"
    row[1] = "Spain F10"
    row[2] = "Hard"
    row[4] = "L"
    row[11] = "Guillermo Platel"
    row[16] = "22.264202601"

    raw = "var morematchmx = " + repr([row]) + ";"
    matches = _clean_matches(_parse_matches(raw))
    result = _calculate_ages(matches, "1986-06-03")

    assert len(result) == 1
    assert result.iloc[0]["opponent"] == "Guillermo Platel"
    assert result.iloc[0]["opponent_age"] == pytest.approx(22.264202601)

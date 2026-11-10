import requests

BASE_URL = "https://www.tennisabstract.com/jsmatches/"


def download_player_data(player_name):
    """Download career match data for a tennis player."""
    clean_name = "".join(player_name.split())
    url = f"{BASE_URL}{clean_name}Career.js"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError(
            f"Unable to retrieve career data for '{player_name}'. "
            "Check the player's name or your connection."
        ) from error

    return response.text

    
import ast
import pandas as pd


def get_player_matches(player_name, player_dob):
    """Return cleaned tennis match data for a player."""

    raw = download_player_data(player_name)

    start = raw.index("[")
    end = raw.index("];", start) + 1
    matches = ast.literal_eval(raw[start:end])

    df = pd.DataFrame(matches)

    player = pd.DataFrame({
        "date": pd.to_datetime(
            df.iloc[:, 0], format="%Y%m%d", errors="coerce"
        ),
        "tournament": df.iloc[:, 1],
        "surface": df.iloc[:, 2],
        "result": df.iloc[:, 4],
        "opponent": df.iloc[:, 11],
        "opponent_dob": pd.to_datetime(
            df.iloc[:, 16], format="%Y%m%d", errors="coerce"
        ),
    })

    player_dob = pd.Timestamp(player_dob)

    player["player_age"] = (
        (player["date"] - player_dob).dt.days / 365.2425
    )

    player["opponent_age"] = (
        (player["date"] - player["opponent_dob"]).dt.days
        / 365.2425
    )

    player["age_difference"] = (
        player["player_age"] - player["opponent_age"]
    )

    player = player.dropna(subset=["date"])
    player = player.sort_values("date")

    return player.reset_index(drop=True)

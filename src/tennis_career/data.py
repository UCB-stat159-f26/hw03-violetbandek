
import ast
import re

import pandas as pd
import requests

BASE_URL = "https://www.tennisabstract.com/jsmatches/"

PLAYER_BIRTHDAYS = {
    "serenawilliams": "1981-09-26",
    "rafaelnadal": "1986-06-03",
}


def download_player_data(player_name):
    """Download a player's career match JavaScript."""
    clean_name = "".join(player_name.split())
    url = f"{BASE_URL}{clean_name}Career.js"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError(
            f"Unable to retrieve data for '{player_name}'. "
            "Check the player's name or internet connection."
        ) from error
    return response.text


def _parse_matches(raw):
    """Convert JavaScript match records into a DataFrame."""
    match = re.search(r"var\s+morematchmx\s*=\s*(\[.*?\]);", raw, re.S)
    if match is None:
        raise ValueError("No valid career match data found.")
    try:
        return pd.DataFrame(ast.literal_eval(match.group(1)))
    except (ValueError, SyntaxError) as error:
        raise ValueError("Unable to parse career match data.") from error


def _clean_matches(df):
    """Extract columns needed for the visualization."""
    return pd.DataFrame({
        "date": pd.to_datetime(df.iloc[:, 0], format="%Y%m%d",
                               errors="coerce"),
        "tournament": df.iloc[:, 1],
        "surface": df.iloc[:, 2],
        "result": df.iloc[:, 4],
        "opponent": df.iloc[:, 11],
        "opponent_age_raw": df.iloc[:, 16],
    })


def _calculate_ages(matches, player_dob):
    """Calculate player and opponent ages at each match."""
    matches = matches.copy()
    dob = pd.Timestamp(player_dob)
    matches["player_age"] = (matches["date"] - dob).dt.days / 365.2425
    raw = matches["opponent_age_raw"].astype(str)
    is_birthdate = raw.str.fullmatch(r"\d{8}").fillna(False)
    opponent_dob = pd.to_datetime(raw.where(is_birthdate),
                                  format="%Y%m%d", errors="coerce")
    birthdate_age = (matches["date"] - opponent_dob).dt.days / 365.2425
    numeric_age = pd.to_numeric(raw.where(~is_birthdate), errors="coerce")
    matches["opponent_age"] = birthdate_age.fillna(numeric_age)
    matches["age_difference"] = matches["player_age"] - matches["opponent_age"]
    return matches.drop(columns="opponent_age_raw")


def get_player_matches(player_name):
    """Retrieve and clean a tennis player's career matches."""
    key = "".join(player_name.lower().split())
    if key not in PLAYER_BIRTHDAYS:
        raise ValueError(f"Unknown player: '{player_name}'.")
    raw = download_player_data(player_name)
    matches = _parse_matches(raw)
    matches = _clean_matches(matches)
    matches = _calculate_ages(matches, PLAYER_BIRTHDAYS[key])
    matches = matches.dropna(subset=["date"])
    return matches.sort_values("date").reset_index(drop=True)

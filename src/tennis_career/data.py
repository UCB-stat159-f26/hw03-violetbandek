
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
    raw = download_player_data(player_name)
    birthday = PLAYER_BIRTHDAYS.get(key)
    if birthday is None:
        birthday = _get_player_birthday(player_name)
    matches = _parse_matches(raw)
    matches = _clean_matches(matches)
    matches = _calculate_ages(matches, birthday)
    matches = matches.dropna(subset=["date"])
    return matches.sort_values("date").reset_index(drop=True)

def _get_player_birthday(player_name):
    """Retrieve a player's birthday from Tennis Abstract."""
    clean_name = "".join(player_name.split())
    for prefix in ("wplayer", "player"):
        url = f"https://www.tennisabstract.com/cgi-bin/{prefix}.cgi"
        try:
            response = requests.get(url, params={"p": clean_name}, timeout=30)
            response.raise_for_status()
        except requests.RequestException:
            continue
        match = re.search(r"\bvar\s+dob\s*=\s*['\"]?(\d{8})", response.text)
        if match:
            return pd.to_datetime(match.group(1), format="%Y%m%d")
    raise ValueError(f"Unable to find birthday for '{player_name}'.")
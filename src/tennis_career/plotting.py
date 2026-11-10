
import matplotlib.pyplot as plt


def _style_axes(ax, player_name):
    ax.xaxis.tick_top()
    ax.tick_params(axis="both", length=0, colors="gray")
    ax.axhline(0, color="gray", linewidth=1)
    ax.grid(axis="both", alpha=0.15)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(f"{player_name}'s Professional Matches",
                 fontsize=13, fontweight="bold", loc="left", pad=65)


def plot_player_matches(matches, player_name="Tennis Player"):
    """Plot match results against player age and opponent age difference."""
    required = {"result", "player_age", "age_difference"}
    if not required.issubset(matches.columns):
        raise ValueError(f"Missing columns: {required - set(matches.columns)}")
    fig, ax = plt.subplots(figsize=(7, 7))
    for result, color, label in [
        ("W", "#36BCE8", "Match won"),
        ("L", "#96358C", "Match lost"),
    ]:
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_difference"],
                   color=color, s=9, alpha=0.85, label=label)
    _style_axes(ax, player_name)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.08),
              ncol=2, frameon=False, fontsize=9)
    fig.subplots_adjust(top=0.78, bottom=0.12)
    return fig

import json
import matplotlib.pyplot as plt

def plot_ground_track_scatter(sats: list[dict]) -> None:
    """Scatter-plot satellite (longitude, latitude) positions on plain matplotlib axes.

    Smoke test only — no projection, no basemap, no labels. Just prove the data
    reaches matplotlib and a window opens with 25 dots in roughly the right shape.

    Args:
        sats: list of propagated satellite dicts, each with 'latitude' and 'longitude' keys.
    """

    lats = [sat["latitude"] for sat in sats]
    longs = [sat["longitude"] for sat in sats]

    plt.scatter(longs, lats)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

if __name__ == "__main__":
    with open("data/propagated_satellites.json") as f:
        satellites = json.load(f)
    plot_ground_track_scatter(satellites)

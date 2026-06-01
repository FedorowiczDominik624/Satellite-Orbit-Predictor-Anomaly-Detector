import json
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def plot_ground_track_scatter(sats: list[dict]) -> None:
    """Scatter-plot satellite (longitude, latitude) positions on plain matplotlib axes.

    Smoke test only — no projection, no basemap, no labels. Just prove the data
    reaches matplotlib and a window opens with 25 dots in roughly the right shape.

    Args:
        sats: list of propagated satellite dicts, each with 'latitude' and 'longitude' keys.
    """

    lats = [sat["latitude"] for sat in sats]
    longs = [sat["longitude"] for sat in sats]

    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
    ax.coastlines()
    ax.gridlines(draw_labels=True)
    ax.scatter(longs, lats, transform=ccrs.PlateCarree())
    ax.set_title("Satellite ground track")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    key_names = ["ISS (ZARYA)", "FREGAT DEB", "SHENZHOU-23 (SZ-23)"]
    for sat in sats:
        if sat["name"] in key_names:
            ax.text(sat["longitude"], sat["latitude"], sat["name"], transform=ccrs.PlateCarree())
    plt.show()



if __name__ == "__main__":
    with open("data/propagated_satellites.json") as f:
        satellites = json.load(f)
    plot_ground_track_scatter(satellites)

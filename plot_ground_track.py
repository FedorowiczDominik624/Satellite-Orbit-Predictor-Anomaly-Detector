import json
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def plot_ground_track_scatter(sats: list[dict]) -> None:
    """Plot satellite ground-track positions on a PlateCarree world map.

    Draws all satellites as a scatter on a cartopy basemap with coastlines and
    labeled latitude/longitude gridlines. Only satellites whose names appear in
    the function's `key_names` list get text labels next to their dot; all others
    are drawn unlabeled to keep the plot readable.

    Args:
        sats: list of propagated satellite dicts, each with 'latitude',
              'longitude', and 'name' keys.
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

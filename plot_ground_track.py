import json
from propagate import propagate
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime, timezone, timedelta

def plot_ground_track_snapshot(sats: list[dict]) -> None:
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
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND)
    ax.coastlines(linewidth=0.75)
    ax.gridlines(draw_labels=True, alpha=0.4)
    ax.scatter(longs, lats, transform=ccrs.PlateCarree(), s=60, edgecolors="white", linewidths=0.75)
    ax.set_title("Satellite ground track")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    key_names = ["ISS (ZARYA)", "FREGAT DEB", "SHENZHOU-23 (SZ-23)"]
    for sat in sats:
        if sat["name"] in key_names:
            ax.text(sat["longitude"], sat["latitude"], sat["name"], transform=ccrs.PlateCarree(), ha="left", va="bottom")
    plt.savefig("docs/ground_track.png", bbox_inches="tight", dpi=150)
    plt.show()

def split_at_wraparound(lons: list[float], lats: list[float]) -> list[tuple[list[float], list[float]]]:
    """Split a polyline into segments at date-line crossings.

    Walks the lons looking for consecutive jumps > 180° in absolute value.
    When found, ends the current segment and starts a new one.

    Returns:
        A list of (segment_lons, segment_lats) tuples. A polyline with no
        wraparound returns a single-tuple list.
    """

    segments = []
    current_lons = []
    current_lats = []

    for i in range(len(lons)):
        if i > 0 and abs(lons[i] - lons[i-1]) > 180:
            segments.append((current_lons, current_lats))
            current_lons = []
            current_lats = []
        current_lons.append(lons[i])
        current_lats.append(lats[i])
    segments.append((current_lons, current_lats))
    return segments

def plot_ground_track_lines(sats: list[dict], hours: float) -> None:
    """plot ground-track polylines for each satellite over 'hours'
    hours of orbit"""


    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND)
    ax.coastlines(linewidth=0.75)
    ax.gridlines(draw_labels=True, alpha=0.4)

    start = datetime.now(timezone.utc)
    step = timedelta(minutes=5)

    timestamps = []
    for a in range(36):
        timestamps.append(start + a * step)

    all_lats = []
    all_lons = []

    for  sat in sats:
        this_sat_lats = []
        this_sat_lons = []
        for t in timestamps:
            lat, lons, _ = propagate(sat, t)
            this_sat_lats.append(lat)
            this_sat_lons.append(lons)
        all_lats.append(this_sat_lats)
        all_lons.append(this_sat_lons)


    for i in range(len(all_lons)):
        sat_lons = all_lons[i]
        sat_lats = all_lats[i]
        segments = split_at_wraparound(sat_lons, sat_lats)
        for seg_lons, seg_lats in segments:
            ax.plot(seg_lons, seg_lats, transform=ccrs.PlateCarree())

    ax.set_title("Satellite ground track over 3 hours")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.savefig("docs/ground_track_lines.png", bbox_inches="tight", dpi=150)
    plt.show()

if __name__ == "__main__":
    # Load propagated sats for the snapshot
    with open("data/propagated_satellites.json") as f:
        propagated_sats = json.load(f)
    plot_ground_track_snapshot(propagated_sats)
    
    # Load raw sats for the lines version
    with open("data/satellites.json") as f:
        raw_sats = json.load(f)
    plot_ground_track_lines(raw_sats, hours=3.0)

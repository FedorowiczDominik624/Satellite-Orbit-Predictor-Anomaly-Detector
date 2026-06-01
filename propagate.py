import json
from pathlib import Path
from datetime import datetime, timezone
from skyfield.api import load, EarthSatellite

def propagate(sat: dict, when: datetime) -> tuple[float, float, float]:
    """Propagate a satellite to a given UTC datetime.

    Args:
        sat: A satellite dict from data/satellites.json (must contain
             'name', 'line1', and 'line2' keys).
        when: A timezone-aware UTC datetime.

    Returns:
        (latitude_deg, longitude_deg, altitude_km) as a 3-tuple of floats.
    """

    timescale = load.timescale()

    satellite_obj = EarthSatellite(sat["line1"], sat["line2"], sat["name"], timescale)

    sky_time = timescale.from_datetime(when)

    ground_point = satellite_obj.at(sky_time).subpoint()

    latitude = ground_point.latitude.degrees
    longitude = ground_point.longitude.degrees
    altitude = ground_point.elevation.km

    return (latitude, longitude, altitude)

def propagate_all(sats: list[dict], when: datetime) -> list[dict]:

    results = []
    for sat in sats:
        try:
            latitude, longitude, altitude = propagate(sat, when)
            new_sat = {**sat, "latitude": latitude, "longitude": longitude, "altitude": altitude}
            results.append(new_sat)
        except Exception as e:
            print(f"Warning: failed to propagate {sat['name']}: {e}")
    return results

if __name__ == "__main__":

    sats_data = json.loads(Path("data/satellites.json").read_text())
    # TEMP TEST: inject a deliberately bad sat to verify error handling
    sats_data.append({"name": "FAKE_BAD_SAT"})

    iss = sats_data[0]  # ISS is first in the list (it's our hello-world satellite)

    right_now = datetime.now(timezone.utc)

    lat, lon, alt = propagate(iss, right_now)

    print(f"{iss['name']} at {right_now.isoformat()}:")
    print(f"  Latitude:  {lat:7.3f}°")
    print(f"  Longitude: {lon:7.3f}°")
    print(f"  Altitude:  {alt:.1f} km")
    

    results = propagate_all(sats_data, right_now)
    print(f"Got {len(results)} satellites")
    
    for sat in results[:3]:
        print(f"{sat['name']}:")          
        print(f"  Latitude:  {sat['latitude']:7.3f}°")
        print(f"  Longitude:  {sat['longitude']:7.3f}°")
        print(f"  Altitude:  {sat['altitude']:.1f} km")
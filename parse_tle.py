"""Parse TLE text from CelesTrak into structured Python dicts."""

def parse_tle_block(name: str, line1: str, line2: str) -> dict:
    """Parse one 3-line TLE block into a dict.
    
    returns: 
        {
            "name": str,             # e.g. "ISS (ZARYA)"
            "satellite_number": int, # NORAD catalog ID, e.g. 25544
            "epoch_year": int,       # 2-digit year as-is, e.g. 26
            "epoch_day": float,      # day of year w/ fractional day,
e.g. 144.12345678
            "inclination_deg": float, # orbital inclination, e.g.
51.6416
       }
    """
    
    clean_name = name.strip()
    satellite_number = int(line1[2:7])
    epoch_year = int(line1[18:20])
    epoch_day = float(line1[20:32])
    inclination_deg = float(line2[8:16])

    parsed = {
        "name": clean_name,
        "satellite_number": satellite_number,
        "epoch_year": epoch_year,
        "epoch_day": epoch_day,
        "inclination_deg": inclination_deg,
    }
    return parsed

def parse_all_tles(text: str) -> list[dict]:
    """Parse a multi-satellite TLE blob into a list of dicts"""
    
    lines = text.splitlines()
    all_tle_data = []

    for i in range(0, len(lines), 3):
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]

        sat_dict = parse_tle_block(name, line1, line2)
        all_tle_data.append(sat_dict)

    return all_tle_data

if __name__ == "__main__":
    name = "ISS (ZARYA)\n"
    line1 = "1 25544U 98067A   26144.51234567  .00012345  00000-0 22334-3 0  9991"
    line2 = "2 25544  51.6416 123.4567 0001234  12.3456 347.6543 15.50123456789012"

    result = parse_tle_block(name, line1, line2)
    print(result)

        # --- test parse_all_tles ---
    fake_blob = """ISS (ZARYA)
1 25544U 98067A   26144.51234567  .00012345  00000-0 22334-3 0  9991
2 25544  51.6416 123.4567 0001234  12.3456 347.6543 15.50123456789012
NOAA 15
1 25338U 98030A   26144.12345678  .00000123  00000-0 12345-3 0  9990
2 25338  98.7654 234.5678 0001234  23.4567 336.5432 14.25987654321098"""

    all_sats = parse_all_tles(fake_blob)
    print(f"\nParsed {len(all_sats)} satellites:")
    for sat in all_sats:
        print(sat)

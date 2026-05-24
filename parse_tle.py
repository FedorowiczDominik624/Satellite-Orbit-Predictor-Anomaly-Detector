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

if __name__ == "__main__":
    name = "ISS (ZARYA)\n"
    line1 = "1 25544U 98067A   26144.51234567  .00012345  00000-0 22334-3 0  9991"
    line2 = "2 25544  51.6416 123.4567 0001234  12.3456 347.6543 15.50123456789012"

    result = parse_tle_block(name, line1, line2)
    print(result)
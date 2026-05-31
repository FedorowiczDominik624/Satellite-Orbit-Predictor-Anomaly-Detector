from fetch_tle import TLE_URL, fetch_tles
from parse_tle import parse_all_tles
from pathlib import Path
import json

def run_pipeline() -> None:
    """Fetches fresh satellite TLE data from CelesTrak, parses it into a list of structured Python dicts, and saves the result to data/satellites.json."""
    
    raw_tle_text = fetch_tles(TLE_URL)
    parsed_sats = parse_all_tles(raw_tle_text)

    output_path = Path("data/satellites.json")

    with open(output_path, "w") as f:
        json.dump(parsed_sats, f, indent=2)

if __name__ == "__main__":
    run_pipeline()
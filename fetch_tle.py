"""Fetch latest TLE data from CelesTrak for the satellite orbit predictor"""

from pathlib import Path
import requests

TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = DATA_DIR / "stations.tle"

def fetch_tles(url: str) -> str:
    """Pull TLE text from CelesTrak. Raises if the request fails"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def save_tles(text: str, output_path: Path) -> None:
    """Write the TLE text to disk, creating the directory if needed"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text)

def main() -> None:
    print(f"Fetching TLEs from {TLE_URL}...")
    tle_text = fetch_tles(TLE_URL)
    save_tles(tle_text, OUTPUT_FILE)

    lines = tle_text.strip().splitlines()
    satellite_count = len(lines) // 3

    print(f"Saved {satellite_count} satellites to {OUTPUT_FILE}")
    print()
    print("First satellite:")
    print(lines[0])  #Name
    print(lines[1])  #TLE line 1
    print(lines[2])  #TLE line 2

if __name__ == "__main__":
    main()

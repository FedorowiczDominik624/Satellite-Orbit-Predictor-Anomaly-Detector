import json
from datetime import datetime, timezone
from propagate import propagate_all
from pathlib import Path

def test_propagate_all_returns_list_of_dicts():
    with open("data/satellites.json") as f:
        sats = json.load(f)
    propagated = propagate_all(sats, datetime.now(timezone.utc))
    assert isinstance(propagated, list)
    assert len(propagated) == len(sats)
    for sat in propagated:
        assert "latitude" in sat
        assert "longitude" in sat
        assert "altitude" in sat

def test_propagate_all_skips_bad_sats():
    with open("data/satellites.json") as f:
        sats = json.load(f)
    bad_sat = {"name": "FAKE BAD SAT"}
    sat_with_bad = sats + [bad_sat]
    propagated = propagate_all(sat_with_bad, datetime.now(timezone.utc))
    assert len(propagated)  == len(sats)
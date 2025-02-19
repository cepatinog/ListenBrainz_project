#!/usr/bin/env python
"""
artist_mapping.py
-----------------
This script processes the musicbrainz_artist.csv file to create a dictionary mapping
artist MBIDs to their textual names.

Usage:
    python artist_mapping.py <input_artist_csv> <output_mapping_json>

Example:
    python artist_mapping.py /mnt/j/MusicBrainz/musicbrainz_artist.csv /mnt/j/MusicBrainz/working/artist_mapping.json
"""

import csv
import json
import sys
import os

def build_artist_mapping(artist_csv):
    """
    Reads the musicbrainz_artist.csv file and returns a dictionary mapping
    artist MBIDs to their textual names.
    
    Parameters:
        artist_csv (str): Path to the musicbrainz_artist.csv file.
        
    Returns:
        dict: A dictionary where keys are artist MBIDs and values are artist names.
    """
    mapping = {}
    with open(artist_csv, "r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            artist_mbid = row.get("artist_mbid")
            name = row.get("name")
            if artist_mbid and name:
                mapping[artist_mbid] = name
    return mapping

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python artist_mapping.py <input_artist_csv> <output_mapping_json>")
        sys.exit(1)
    
    artist_csv = sys.argv[1]
    output_file = sys.argv[2]
    
    mapping = build_artist_mapping(artist_csv)
    print(f"Built mapping for {len(mapping)} artists.")
    
    # Save the mapping as a JSON file for later use.
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"Mapping saved to {output_file}")

#!/usr/bin/env python
"""
canonicalize.py
---------------
This script processes user listening events by joining user–MSID data with the filtered
MSID mapping, applying canonical redirect mapping, and extracting artist information from the canonical
metadata file. The final output is a CSV mapping each user_id to an artist_id (derived from the recording's artist credit).

Usage:
    python canonicalize.py <userid_msid_csv> <small_msid_mapping_csv> <canonical_redirect_file> <canonical_metadata_file> <output_user_artist_csv>

Example:
    python canonicalize.py /mnt/j/MusicBrainz/working/userid-msid.csv \
                            /mnt/j/MusicBrainz/working/small_msid_mapping.csv \
                            /mnt/j/MusicBrainz/canonical_recording_redirect.csv.zst \
                            /mnt/j/MusicBrainz/canonical_musicbrainz_data.csv.zst \
                            /mnt/j/MusicBrainz/working/userid-artist.csv
"""

import csv
import sys
import os
from tqdm import tqdm

# Ensure the project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.file_utils import decompress_if_needed

def load_user_msids(userid_msid_csv):
    """
    Loads the user_id and recording_msid pairs from the extracted CSV.
    
    Returns a list of dictionaries with keys: 'user_id', 'recording_msid'
    """
    data = []
    with open(userid_msid_csv, "r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            data.append({
                "user_id": row["user_id"],
                "recording_msid": row["recording_msid"]
            })
    print(f"Loaded {len(data)} user listening events from {userid_msid_csv}")
    return data

def load_filtered_mapping(filtered_mapping_csv):
    """
    Loads the filtered mapping (MSID -> MBID) from CSV.
    
    Returns a dictionary mapping recording_msid -> recording_mbid.
    """
    mapping = {}
    with open(filtered_mapping_csv, "r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            msid = row["recording_msid"]
            mbid = row["recording_mbid"]
            mapping[msid] = mbid
    print(f"Loaded {len(mapping)} MSID-to-MBID mappings from {filtered_mapping_csv}")
    return mapping

def load_canonical_redirect(redirect_file):
    """
    Loads the canonical redirect mapping from the canonical redirect CSV.
    
    Returns a dictionary mapping non-canonical MBID -> canonical MBID.
    """
    # Decompress the redirect file if needed.
    redirect_file = decompress_if_needed(redirect_file)
    
    redirect = {}
    with open(redirect_file, "r", encoding="utf-8", errors="replace") as fp:
        reader = csv.DictReader(fp)
        # Assume header contains columns: "recording_mbid" and "canonical_recording_mbid"
        for row in reader:
            non_canonical = row.get("recording_mbid")
            canonical = row.get("canonical_recording_mbid")
            if non_canonical and canonical:
                redirect[non_canonical] = canonical
    print(f"Loaded {len(redirect)} canonical redirects from {redirect_file}")
    return redirect

def load_canonical_metadata(metadata_file):
    """
    Loads the canonical metadata which includes artist information.
    
    Returns a dictionary mapping canonical recording MBID -> first artist MBID.
    
    The metadata file is assumed to have a header with at least these columns:
       - recording_mbid
       - artist_mbids (a string containing one or more artist MBIDs, comma-separated)
       
    For simplicity, we take the first artist MBID from the 'artist_mbids' field.
    """
    metadata = {}
    # Decompress if needed.
    metadata_file = decompress_if_needed(metadata_file)
    
    with open(metadata_file, "r", encoding="utf-8", errors="replace") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            rec_mbid = row.get("recording_mbid")
            artist_mbids = row.get("artist_mbids")
            if rec_mbid and artist_mbids:
                # Split the artist_mbids by comma and take the first entry.
                first_artist = artist_mbids.split(",")[0].strip()
                metadata[rec_mbid] = first_artist
    print(f"Loaded artist metadata for {len(metadata)} recordings from {metadata_file}")
    return metadata


def process_user_artist(userid_msid_csv, filtered_mapping_csv, redirect_file, metadata_file, output_csv):
    """
    Joins the user listening data with the filtered MSID mapping, applies canonical redirects,
    and then extracts artist information using the canonical metadata.
    
    Outputs a CSV file with columns: user_id, artist_id.
    """
    # Load data
    user_data = load_user_msids(userid_msid_csv)
    msid_to_mbid = load_filtered_mapping(filtered_mapping_csv)
    redirect = load_canonical_redirect(redirect_file)
    metadata = load_canonical_metadata(metadata_file)
    
    # Process each user listening event:
    # 1. Map recording_msid to recording_mbid using the filtered mapping.
    # 2. Apply canonical redirect if available.
    # 3. Look up artist information in the metadata.
    total_events = 0
    converted_events = 0
    output_rows = []
    
    for event in tqdm(user_data, desc="Processing user events"):
        total_events += 1
        msid = event["recording_msid"]
        user_id = event["user_id"]
        mbid = msid_to_mbid.get(msid)
        if not mbid:
            # Skip if no mapping is available.
            continue
        # Apply canonical redirect if available.
        canonical_mbid = redirect.get(mbid, mbid)
        # Look up artist info in metadata.
        artist_id = metadata.get(canonical_mbid)
        if not artist_id:
            continue
        # Create an output row: we map the listen event to an artist.
        output_rows.append({
            "user_id": user_id,
            "artist_id": artist_id
        })
        converted_events += 1
    
    # Ensure the output directory exists.
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    # Write out the final user-artist mapping.
    with open(output_csv, "w", newline='', encoding="utf-8") as fp:
        fieldnames = ["user_id", "artist_id"]
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)
    
    print(f"Processed {total_events} user events; converted {converted_events} events to user-artist pairs.")
    print(f"Output written to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python canonicalize.py <userid_msid_csv> <filtered_mapping_csv> <canonical_redirect_file> <canonical_metadata_file> <output_user_artist_csv>")
        sys.exit(1)
    
    userid_msid_csv = sys.argv[1]
    filtered_mapping_csv = sys.argv[2]
    redirect_file = sys.argv[3]
    metadata_file = sys.argv[4]
    output_csv = sys.argv[5]
    
    process_user_artist(userid_msid_csv, filtered_mapping_csv, redirect_file, metadata_file, output_csv)

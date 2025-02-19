#!/usr/bin/env python
"""
filter_mapping.py
-----------------
This script filters the ListenBrainz MSID mapping file by keeping only the rows corresponding
to the MSIDs present in our 'userid-msid.csv' file and meeting a specified quality criterion.
It outputs a smaller mapping file that can be loaded into memory for subsequent processing.

Usage:
    python filter_mapping.py <userid_msid_csv> <msid_mapping_file> <output_filtered_mapping_csv>

Example:
    python filter_mapping.py /mnt/j/MusicBrainz/working/userid-msid.csv \
                              /mnt/j/MusicBrainz/listenbrainz_msid_mapping.csv-003.zst \
                              /mnt/j/MusicBrainz/working/small_msid_mapping.csv
"""

import sys
import os
import csv
from tqdm import tqdm

# Ensure the project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.file_utils import decompress_if_needed

def load_unique_msids(userid_msid_csv):
    """
    Loads the unique MSIDs from the provided CSV file.

    Parameters:
        userid_msid_csv (str): Path to the CSV file containing columns "user_id" and "recording_msid".

    Returns:
        A set of unique MSID strings.
    """
    unique_msids = set()
    with open(userid_msid_csv, "r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            msid = row["recording_msid"]
            unique_msids.add(msid)
    print(f"Loaded {len(unique_msids)} unique MSIDs from {userid_msid_csv}")
    return unique_msids

def filter_mapping(userid_msid_csv, mapping_file, output_file, acceptable_qualities={"exact_match", "high_quality"}):
    """
    Filters the ListenBrainz MSID mapping file to include only rows with MSIDs present in our extracted CSV
    and with an acceptable match quality.
    
    Parameters:
        userid_msid_csv (str): Path to the CSV with user_id and recording_msid.
        mapping_file (str): Path to the large ListenBrainz MSID mapping file.
        output_file (str): Path where the filtered mapping CSV will be written.
        acceptable_qualities (set): Set of acceptable quality levels.
        
    The mapping file is assumed to have a header with at least these columns:
        recording_msid, recording_mbid, match_type, ...
    """
    # Decompress the mapping file if needed
    mapping_file = decompress_if_needed(mapping_file)
    
    unique_msids = load_unique_msids(userid_msid_csv)
    
    total_rows = 0
    kept_rows = 0

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(mapping_file, "r", encoding="utf-8", errors="replace") as infile, \
         open(output_file, "w", newline='', encoding="utf-8") as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        # Iterate over the mapping file with a progress bar
        for row in tqdm(reader, desc="Filtering mapping file"):
            total_rows += 1
            # Use the correct column names: "recording_msid" and "match_type"
            msid = row.get("recording_msid")
            quality = row.get("match_type")
            if msid in unique_msids and quality in acceptable_qualities:
                writer.writerow(row)
                kept_rows += 1

    print(f"Processed {total_rows} rows from {mapping_file}")
    print(f"Kept {kept_rows} rows in the filtered mapping file: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter_mapping.py <userid_msid_csv> <msid_mapping_file> <output_filtered_mapping_csv>")
        sys.exit(1)
    
    userid_msid_csv = sys.argv[1]
    mapping_file = sys.argv[2]
    output_file = sys.argv[3]

    filter_mapping(userid_msid_csv, mapping_file, output_file)

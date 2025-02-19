#!/usr/bin/env python
"""
aggregate_counts.py
-------------------
This script aggregates user-artist listen events to create a matrix of listen counts.
It reads the "userid-artist.csv" file (which maps each individual event to an artist),
sums up the counts for each (user, artist) pair, and writes the aggregated data to a new CSV file.

Usage:
    python aggregate_counts.py <input_user_artist_csv> <output_user_artist_counts_csv>

Example:
    python aggregate_counts.py /mnt/j/MusicBrainz/working/userid-artist.csv /mnt/j/MusicBrainz/working/userid-artist-counts.csv
"""

import csv
import sys
import os
from collections import defaultdict

def aggregate_listens(input_file, output_file):
    """
    Aggregates user-artist events into listen counts.
    
    Parameters:
        input_file (str): Path to the CSV file with columns "user_id" and "artist_id".
        output_file (str): Path to the output aggregated CSV file with columns "user_id,artist_id,listen_count".
    """
    # Dictionary to hold aggregated counts for each (user_id, artist_id) pair.
    counts = defaultdict(int)
    
    # Read the input file and count the events.
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            key = (row["user_id"], row["artist_id"])
            counts[key] += 1
    
    # Ensure the output directory exists.
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the aggregated counts to the output CSV file.
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['user_id', 'artist_id', 'listen_count']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for (user_id, artist_id), count in counts.items():
            writer.writerow({
                'user_id': user_id,
                'artist_id': artist_id,
                'listen_count': count
            })
    
    print(f"Aggregated counts written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python aggregate_counts.py <input_user_artist_csv> <output_user_artist_counts_csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    aggregate_listens(input_file, output_file)

#!/usr/bin/env python
"""
extract_listens.py
------------------
This script reads a ListenBrainz JSON Lines file, inspects its structure by printing
a few sample records, and then extracts the 'user_id' and 'recording_msid' fields into a CSV file.

Usage:
    python extract_listens.py <input_file> <output_csv>

Example:
    python extract_listens.py /mnt/j/MusicBrainz/1.listens.zst /mnt/j/MusicBrainz/working/userid-msid.csv
"""

import json
import csv
import sys
import os
import subprocess
from tqdm import tqdm

def inspect_file(input_file, num_lines=5):
    """
    Reads and prints the first few lines of the JSON Lines file to inspect its structure.

    Parameters:
        input_file (str): Path to the JSON Lines file.
        num_lines (int): Number of lines to inspect.
    """
    print(f"Inspecting the first {num_lines} lines of {input_file}:")
    with open(input_file, 'r', encoding='utf-8') as infile:
        for i in range(num_lines):
            line = infile.readline().strip()
            if not line:
                break
            try:
                record = json.loads(line)
                print(json.dumps(record, indent=4))
            except json.JSONDecodeError as e:
                print(f"Error decoding line {i+1}: {e}")

def extract_listen_events(input_file, output_csv):
    """
    Reads the ListenBrainz JSON Lines file, extracts user_id and recording_msid,
    and writes the results to a CSV file. Displays a progress bar indicating the progress.

    Parameters:
        input_file (str): Path to the JSON Lines input file.
        output_csv (str): Path to the CSV file to output extracted data.
    """
    total_lines = 0
    extracted_lines = 0

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Get the total size of the file in bytes for the progress bar.
    total_size = os.path.getsize(input_file)

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        
        writer = csv.writer(outfile)
        writer.writerow(['user_id', 'recording_msid'])
        
        # Create a progress bar based on file size
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Processing") as pbar:
            for line in infile:
                total_lines += 1
                # Update progress bar by the number of bytes in the line
                pbar.update(len(line))
                try:
                    record = json.loads(line)
                    user_id = record.get('user_id')
                    recording_msid = record.get('recording_msid')
                    
                    if user_id and recording_msid:
                        writer.writerow([user_id, recording_msid])
                        extracted_lines += 1
                except json.JSONDecodeError as e:
                    print(f"Error parsing line {total_lines}: {e}")
    
    print(f"\nFinished processing {total_lines} lines.")
    print(f"Extracted {extracted_lines} valid records to '{output_csv}'.")

def decompress_if_needed(input_path):
    """
    Checks if the input file is compressed (.zst) and decompresses it if needed.
    Returns the path to the decompressed file.
    """
    if input_path.endswith('.zst'):
        # Remove exactly 4 characters (".zst") from the end
        decompressed_path = input_path[:-4]
        if not os.path.exists(decompressed_path):
            print(f"Decompressing {input_path} to {decompressed_path} ...")
            subprocess.run(["unzstd", input_path], check=True)
        return decompressed_path
    return input_path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_listens.py <input_file> <output_csv>")
        sys.exit(1)
    
    raw_input_file = sys.argv[1]
    output_csv = sys.argv[2]
    
    # Decompress the file if needed
    input_file = decompress_if_needed(raw_input_file)
    
    # Inspect the file structure by printing the first few lines
    inspect_file(input_file, num_lines=5)
    
    # Extract data to CSV with a progress bar
    extract_listen_events(input_file, output_csv)

# src/utils/config.py
import os

# Base path for your external drive where raw files are stored.
EXTERNAL_DRIVE_PATH = "/mnt/j/MusicBrainz"

# Raw data files are stored directly under the external drive
RAW_DATA_PATH = EXTERNAL_DRIVE_PATH

# Directory for processed (working) files
WORKING_DIR = os.path.join(EXTERNAL_DRIVE_PATH, "working")

# Number of lines to inspect from a raw JSON Lines file
NUM_INSPECT_LINES = 5

# Extension for compressed files
COMPRESSED_EXTENSION = ".zst"

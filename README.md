# ListenBrainz Collaborative Filtering Project

**Author:** Carlos Patiño
**Teachers:** Alastair Porter and Dmitry Bogdanov
**Date:** 19 February 2025

## Overview

This project builds a collaborative filtering model to identify similar musical artists based on user listening history from ListenBrainz. Given the massive scale of the raw data (over 90 million listening events spanning 10+ years), our pipeline is designed to efficiently process and convert this data into a user–artist matrix. For development, we focused on data from the first month of 2024, with the intention of scaling the approach to cover the entire year.

The final output is a matrix of user IDs, artist MBIDs, and play counts that is used to train an Alternating Least Squares (ALS) model using the Implicit library. This model generates artist similarity recommendations that we have compared with those from external services like Spotify and Last.fm.

## Data and Environment

- **Raw Data Location:**  
  All raw data is stored on an external hard drive mounted at `J:\MusicBrainz`.
  
- **Processed Data:**  
  Processed files are located in the `data/processed` directory. For example, the final aggregated file `userid-artist-counts.csv` is stored there.

- **Development Environment:**  
  The project is developed locally under WSL (Ubuntu). All paths within the project point to our external hard drive (e.g., `/mnt/j/MusicBrainz/`).

## Repository

The complete code for the project is available at:  
[https://github.com/cepatinog/ListenBrainz_project](https://github.com/cepatinog/ListenBrainz_project)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/cepatinog/ListenBrainz_project.git
   cd ListenBrainz_project

2. **Create and Activate the Conda Environment:**

   ```bash
   conda env create -f environment.yml
   conda activate listenbrainz_env

3. **Install Additional Dependencies (if needed):**

   ```bash
   pip install -r requirements.txt

**Project Structure**

```
LISTENBRAINZ-PROJECT [WSL: UBUNTU]
│
├── data
│   ├── external         # Additional external datasets (e.g., full MusicBrainz dumps)
│   ├── processed        # Processed files (e.g., userid-artist-counts.csv)
│   └── raw              # Raw ListenBrainz data and mapping files
│
├── notebooks            # Jupyter notebooks for data preprocessing, modeling, and final report
│   ├── listenbrainz_model.py  # Helper module for model building
│   ├── Modeling.ipynb         # Code for building and querying the ALS model
│   ├── Preprocessing.ipynb    # Steps for data extraction and processing
│   └── Report.ipynb           # Final report and analysis
│
├── src                  # Source code for project modules
│   ├── preprocessing    # Data processing scripts
│   │   ├── aggregate_counts.py
│   │   ├── artist_mapping.py
│   │   ├── canonicalize.py
│   │   ├── convert_msids.py
│   │   ├── extract_listens.py
│   │   └── filter_mapping.py
│   └── utils            # Utility functions and configuration files
│       ├── config.py
│       └── file_utils.py
│
├── .gitignore
├── environment.yml      # Conda environment specification
├── README.md
└── requirements.txt     # Additional pip dependencies

```
# Usage

## Data Preprocessing

### Extract Listen Events
Run the extraction script to generate `userid-msid.csv`:

```bash
python src/preprocessing/extract_listens.py /mnt/j/MusicBrainz/1.listens.zst /mnt/j/MusicBrainz/working/userid-msid.csv

```

### Filter MSID Mapping
   ```
   Filter the massive MSID mapping file to produce small_msid_mapping.csv:
   ```

### Canonicalize and Extract Artist Info
Join user–MSID data with the filtered mapping, apply canonical redirects, and extract artist information:
   
   ```
   python src/preprocessing/canonicalize.py /mnt/j/MusicBrainz/working/userid-msid.csv /mnt/j/MusicBrainz/working/small_msid_mapping.csv /mnt/j/MusicBrainz/canonical_recording_redirect.csv.zst /mnt/j/MusicBrainz/canonical_musicbrainz_data.csv.zst /mnt/j/MusicBrainz/working/userid-artist.csv
   ```
### Aggregate Listen Counts
Aggregate individual user–artist events into userid-artist-counts.csv:
   ```
   python src/preprocessing/aggregate_counts.py /mnt/j/MusicBrainz/working/userid-artist.csv /mnt/j/MusicBrainz/working/userid-artist-counts.csv
   ```

### Build Artist Mapping
Create a mapping of artist MBIDs to names:
   ```
   python src/preprocessing/artist_mapping.py /mnt/j/MusicBrainz/musicbrainz_artist.csv /mnt/j/MusicBrainz/working/artist_mapping.json
   ```

## Model Building and Querying
Use the provided `listenbrainz_model.py` and the notebooks in the `notebooks` directory (e.g., `Modeling.ipynb`) to:

- Load the data matrix from `userid-artist-counts.csv`
- Train the ALS model using BM25 weighting
- Query the model for similar artists and display the results with human-readable names

## Real-World Examples
Real-world examples are provided in the notebooks, demonstrating similar artist recommendations for well-known bands such as:

- **The Beatles**: `b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d`
- **Soda Stereo**: `3f8a5e5b-c24b-4068-9f1c-afad8829e06b`

## Model Evaluation

### Observations
Our ALS model generated intuitive similar artist recommendations. For example, similar artists for The Beatles included **John Lennon, The Rolling Stones, and The Who**.

### External Comparison
When compared with recommendations from **Spotify** and **Last.fm**, many of the core suggestions were similar, though differences in ranking and additional recommendations were noted.

### Dataset Considerations
Our current model is built using data from **January 2024**. Scaling the pipeline to process all **12 months** will likely yield a more robust and representative model, akin to larger datasets like the **Last.fm 360K dataset**.

## Conclusion
This project demonstrates an end-to-end pipeline—from data extraction and preprocessing to collaborative filtering model training and evaluation—using **ListenBrainz** data. Although developed on a subset of data, the system is fully scalable and modular. All code is available in our **GitHub repository**, and all data paths point to our external hard drive (`J:\MusicBrainz`). The final aggregated file (`userid-artist-counts.csv`) is located in the `data/processed` directory.

**Note:** All code used in this project is fully documented and reproducible. Any use of **LLMs** or coding assistants has been documented in the report.

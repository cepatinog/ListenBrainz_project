# ListenBrainz Collaborative Filtering Project

## Overview
This project processes the ListenBrainz dataset to build a collaborative filtering model that identifies similar musical artists based on user listening history.

## Directory Structure
- **data/**: Raw input files.
- **scratch/**: Temporary files during processing.
- **working/**: Processed files ready for modeling.
- **notebooks/**: Jupyter notebooks for exploration.
- **src/**: Python scripts for data processing and modeling.
- **reports/**: Final report and documentation.

## Setup Instructions
1. Clone this repository.
2. Create and activate the conda environment:
   ```bash
   conda create -n listenbrainz_env python=3.10.16 -y
   conda activate listenbrainz_env
3. Install dependencies:
   ```bash
   conda install -c conda-forge numpy pandas scipy matplotlib seaborn jupyterlab -y
   pip install implicit h5py zstandard musicbrainzngs squarify

4. Start JupyterLab:
   ```bash
   jupyter lab
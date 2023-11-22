#!/bin/bash

# Stop on any error
set -e

# Activate Conda environment
source /miniconda3/etc/profile.d/conda.sh  # This might be something like '/miniconda3/etc/profile.d/conda.sh'
conda activate pyspark_env


# Change to the directory containing the scripts
cd ~/bill_subject_classification/scripts

# Run pipeline in sequence
python fetch_data.py
python data_preprocessing.py
python zero_shot_classification.py
python neo4j_ingestion.py

# Deactivate the Python environment
conda deactivate

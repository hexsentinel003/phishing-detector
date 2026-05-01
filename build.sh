#!/bin/bash
set -e

echo "Creating data directory..."
mkdir -p data

echo "Downloading dataset..."
echo "Dataset already included in repo, skipping download..."

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Training model..."
python model/rebuild_and_train.py

echo "Build complete!"
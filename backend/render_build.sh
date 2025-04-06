#!/bin/bash
# This script runs during the build phase on Render

# Install dependencies
pip install -r requirements.txt

# Create database and populate with data
python app/populate_db.py

echo "Build completed successfully!" 
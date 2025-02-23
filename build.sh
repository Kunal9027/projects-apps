# using build.sh to collect static files on render beacuse it is not possible to run collectstatic command directly on render free tier this file help to run collectstatic command on render free tier 

#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
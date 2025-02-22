# using build.sh to collect static files on render beacuse it is not possible to run collectstatic command directly on render free tier this file help to run collectstatic command on render free tier 

#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
python -m pip install --upgrade pip

# Install platform-specific requirements
if [ "$(uname)" == "Linux" ]; then
    pip install -r requirements.txt --no-deps
    pip install django yt-dlp instaloader browser-cookie3 gunicorn
else
    pip install -r requirements.txt
fi

# Run Django commands
python manage.py collectstatic --no-input
python manage.py migrate
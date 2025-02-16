# using build.sh to collect static files on render beacuse it is not possible to run collectstatic command directly on render free tier this file help to run collectstatic command on render free tier 

#!/usr/bin/env bash
python manage.py collectstatic --noinput
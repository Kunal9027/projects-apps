# using build.sh to collect static files on render beacuse it is not possible to run collectstatic command directly on render free tier this file help to run collectstatic command on render free tier 

python manage.py collectstatic --no-input  #static files collection

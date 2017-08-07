# Clean up cached static files
rm -r static Website/static/min

# Sync back-end repo with GitHub
git fetch --all
git reset --hard origin/master

# Sync front-end repo with GitHub
cd Website/static
git fetch --all
git reset --hard origin/master
cd ../..

# Compress and collect static files
python manage.py compress
python manage.py collectstatic

# Restart Gunicorn and Nginx
systemctl restart gunicorn
systemctl restart nginx

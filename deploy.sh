#!/usr/bin/env bash

# Clean up cached static files
rm -r static Website/static/min

# Backup database file
mv db.sqlite3 db.save

# Sync back-end repo with GitHub
git fetch --all
git reset --hard origin/master

# Sync front-end repo with GitHub
cd Website/static
git fetch --all
git reset --hard origin/master
cd ../..

# Restore database file
mv db.save db.sqlite3

# Compress and collect static files
python3 manage.py compress
python3 manage.py collectstatic

# Clean up uncompressed static files
rm -r static/css static/js

# Restart Gunicorn and Nginx
systemctl restart gunicorn
systemctl restart nginx

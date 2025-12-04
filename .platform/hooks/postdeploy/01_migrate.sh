#!/bin/bash

# Activate virtual environment
source /var/app/venv/*/bin/activate

# Navigate to application directory
cd /var/app/current

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

echo "Post-deploy commands completed successfully"


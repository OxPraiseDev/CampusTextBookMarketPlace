#!/usr/bin/env bash
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files
python manage.py collectstatic --no-input

# 3. Apply database migrations
python manage.py migrate

# 4. Create a superuser if it doesn't exist (using environment variables)
python manage.py createsuperuser --no-input || echo "Superuser already exists."
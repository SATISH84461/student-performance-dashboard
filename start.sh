#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🗃️ Applying database migrations..."
python manage.py migrate

echo "🚀 Starting Django development server..."
python manage.py runserver 0.0.0.0:8000

#!/bin/sh

# Check if the 'db_initialized' marker file exists
if [ ! -f /app/db_initialized ]; then
  # File doesn't exist, assume first-time setup needed
  echo "Running migrations..."
  python manage.py makemigrations --noinput
  python manage.py migrate

  # Create an empty file as a marker for future container starts
  touch /app/db_initialized
else
  echo "Migrations not required."
fi

# Continue to the main command
exec "$@"

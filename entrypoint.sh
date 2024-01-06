#!/bin/sh

# Wait for PostgreSQL to become available.
# You might need to modify this part to suit your specific needs.
echo "Waiting for PostgreSQL..."
while ! nc -z jobson_postgres_db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
alembic upgrade head

# Start your application
exec "$@"

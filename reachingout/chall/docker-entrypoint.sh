#!/bin/sh

# Save the flag to disk
echo $FLAG > /etc/flag/flag.txt

# Init postgres
su postgres -c "initdb -D /var/lib/postgresql/data"

# Start postgres
su postgres -c "pg_ctl -D /var/lib/postgresql/data -l /var/lib/postgresql/logfile start"

# Wait for PostgreSQL to start
sleep 5

# Create database and user
su postgres -c "createdb company_directory"

python init_db.py

su user -c "python server.py"

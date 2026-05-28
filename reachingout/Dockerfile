FROM python:3.9-alpine

# Install system dependencies
RUN apk add --no-cache postgresql postgresql-dev supervisor
WORKDIR /app

# Copy and install Python requirements
COPY chall/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy application files
COPY chall/ /app/

# Set up PostgreSQL
RUN mkdir -p /run/postgresql && chown postgres:postgres /run/postgresql
RUN mkdir -p /var/lib/postgresql/data && chown postgres:postgres /var/lib/postgresql/data
RUN adduser -u 1337 --disabled-password user

# Expose port
EXPOSE 8000

# Start supervisord
CMD ["/app/docker-entrypoint.sh"]

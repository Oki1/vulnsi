FROM python:3.13-alpine

WORKDIR /app

RUN pip install --no-cache-dir Flask && mkdir -p /app/db

COPY app.py /app/
COPY templates /app/templates
COPY static /app/static

EXPOSE 8000

CMD ["python3", "app.py"]

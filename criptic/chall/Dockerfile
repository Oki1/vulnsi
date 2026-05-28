FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-flask \
    nginx

WORKDIR /app
COPY . /app/

COPY nginx.conf /etc/nginx/sites-available/default
RUN mkdir -p /app/templates

EXPOSE 80

RUN echo "#!/bin/bash\n\
nginx\n\
python3 /app/main.py &\n\
tail -f /dev/null" > /app/start.sh && \
chmod +x /app/start.sh

CMD ["/app/start.sh"]

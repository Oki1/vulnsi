FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py init.py security.py ./

RUN chown -R www-data:www-data .

EXPOSE 5000
USER www-data

CMD [ "flask", "--app", "app" , "run", "-h", "0.0.0.0", "-p", "5000"]

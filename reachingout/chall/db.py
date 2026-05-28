import os

import psycopg2


def get_db():
    conn = psycopg2.connect(
        dbname="company_directory",
        user="postgres",
        password=os.environ.get("POSTGRES_ROOT_PASSWORD", "root"),
        host="localhost"
    )
    conn.autocommit = True
    return conn

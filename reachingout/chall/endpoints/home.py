import psycopg2.extras
from flask import Blueprint, render_template, request, send_file

from db import get_db

bp = Blueprint('home', __name__)

def build_query(args):
    # Remove empty values
    query = {}
    for key, value in args.items():
        if value := value.strip():
            query[key] = value

    where_string = ""
    if len(query) > 0:
        where_string = "WHERE " + ' AND '.join(f'{key} ILIKE %s' for key in query.keys())

    return where_string


@bp.route('/', methods=['GET'])
def home():
    # Remove empty values
    query = {}
    for key, value in request.args.items():
        if value := value.strip():
            query[key] = value

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    qq = "SELECT * FROM directory " + build_query(query) + " LIMIT 10"
    print(qq, flush=True)

    # Execute query - uses vars= to avoid SQL injection
    cur.execute(qq, vars=list(query.values()))
    items = cur.fetchall()

    # Close connections
    cur.close()
    conn.close()

    return render_template('index.html', items=items, search_query=query)

@bp.route('/export', methods=['GET'])
def export():
    filename = '/tmp/export.csv'

    # Remove empty values
    query = {}
    for key, value in request.args.items():
        if value := value.strip():
            query[key] = value
    print(query)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    qq = "COPY directory " + build_query(query) + " TO '" + filename + "' DELIMITER ',' CSV HEADER"
    print(qq, flush=True)

    # Execute query - uses vars= to avoid SQL injection
    cur.execute(qq, vars=list(query.values()))

    # Close connections
    cur.close()
    conn.close()

    # Serve the file
    return send_file(filename, as_attachment=True)

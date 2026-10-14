import os
import sqlite3
import subprocess
import threading
from flask import Flask, request, render_template, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vuln-tour-secret")

FLAG = os.environ.get("FLAG", "dctf{part1_part2_part3_part4}")
DB_PATH = os.environ.get("DB_PATH", "/app/db/app.db")
RCE_FLAG_PATH = os.environ.get("RCE_FLAG_PATH", "/flag_part4.txt")
RCE_FLAG_FALLBACK = "/tmp/flag_part4.txt"
CURRENT_USER_ID = 1

reported_urls = []
state_lock = threading.Lock()


def split_flag(flag):
    size = len(flag) // 4
    return [flag[0:size], flag[size:2 * size], flag[2 * size:3 * size], flag[3 * size:]]


PARTS = split_flag(FLAG)

PROFILES = [
    {"id": 1, "name": "guest", "secret": "no secret here"},
    {"id": 2, "name": "Alice Smith", "secret": "no secret here"},
    {"id": 3, "name": "Bob Jones", "secret": "no secret here"},
    {"id": 4, "name": "Carol White", "secret": "no secret here"},
    {"id": 5, "name": "JOHN FLAG", "secret": PARTS[2]},
    {"id": 6, "name": "Dave Brown", "secret": "no secret here"},
    {"id": 7, "name": "Eve Black", "secret": "no secret here"},
    {"id": 8, "name": "Frank Green", "secret": "no secret here"},
]


def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS secret_flag")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "s3cr3t_admin_pw", "admin"))
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("guest", "guest", "member"))
    cursor.execute("CREATE TABLE secret_flag (part TEXT)")
    cursor.execute("INSERT INTO secret_flag (part) VALUES (?)", (PARTS[0],))
    connection.commit()
    connection.close()


def init_rce_flag():
    for path in (RCE_FLAG_PATH, RCE_FLAG_FALLBACK):
        try:
            with open(path, "w") as handle:
                handle.write(PARTS[3] + "\n")
        except OSError:
            continue


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sqli", methods=["GET", "POST"])
def sqli():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        query = "SELECT id, username FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        connection = sqlite3.connect(DB_PATH)
        rows = []
        try:
            rows = connection.execute(query).fetchall()
        except sqlite3.Error as error:
            message = "SQL error: " + str(error)
        finally:
            connection.close()
        if rows:
            session["user"] = rows[0][1]
            return redirect(url_for("sqli_search"))
        if not message:
            message = "Invalid credentials"
    return render_template("sqli.html", message=message)


@app.route("/sqli/search")
def sqli_search():
    if not session.get("user"):
        return redirect(url_for("sqli"))
    query = request.args.get("q", "")
    results = []
    message = ""
    if query:
        sql = "SELECT username FROM users WHERE username LIKE '%" + query + "%'"
        connection = sqlite3.connect(DB_PATH)
        try:
            results = [row[0] for row in connection.execute(sql).fetchall()]
        except sqlite3.Error as error:
            message = "SQL error: " + str(error)
        finally:
            connection.close()
    return render_template("search.html", user=session.get("user"), results=results, query=query, message=message)


@app.route("/xss")
def xss():
    query = request.args.get("q", "")
    return render_template("xss.html", query=query)


@app.route("/xss/report", methods=["POST"])
def xss_report():
    url = request.form.get("url", "").strip()
    if url:
        with state_lock:
            reported_urls.append(url)
    return render_template("reported.html")


@app.route("/bot/queue")
def bot_queue():
    with state_lock:
        items = list(reported_urls)
        reported_urls.clear()
    return jsonify(items)


@app.route("/idor")
def idor():
    return render_template("idor.html", current_user_id=CURRENT_USER_ID)


@app.route("/api/profile", methods=["POST"])
def api_profile():
    data = request.get_json(silent=True) or {}
    user_id = data.get("id", request.form.get("id"))
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid id"}), 400
    for profile in PROFILES:
        if profile["id"] == user_id:
            return jsonify(profile)
    return jsonify({"error": "not found"}), 404


@app.route("/rce", methods=["GET", "POST"])
def rce():
    output = ""
    host = "127.0.0.1"
    if request.method == "POST":
        host = request.form.get("host", "")
        command = "ping -c 1 " + host
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "command timed out"
    return render_template("rce.html", output=output, host=host)


init_database()
init_rce_flag()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)

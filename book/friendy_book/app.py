import os
from flask import Flask, request, session, redirect, url_for, g
from html import escape
from security import compare_password
import sqlite3
import secrets
import sys
import init

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

DATABASE = "./sqlite3.db"
FLAG = os.environ["DCTF_FLAG"]


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


with app.app_context():
    init.init_database(get_db().cursor())


def init_session(username: str):
    db = get_db().cursor()
    r = db.execute("SELECT username, name FROM users WHERE username = ?", [username])
    u = r.fetchone()
    if not u:
        return None
    return {
        "username": u[0],
        "name": u[1],
        "role": "user",
        "default_sort": "ASC",
    }


def flash_msg():
    msg = request.args.get("msg", "")
    msg = ("<p><b>" + escape(msg) + "</b></p>") if msg else ""
    return msg


@app.get("/search")
def search():
    active_user = session.get("user")
    if not active_user:
        return redirect(url_for("login") + "?msg=Please+log+in")

    user_preference = active_user["default_sort"]
    q = request.args.get("query", "")
    q = f"%{q}%"
    db = get_db().cursor()
    print("SELECT name FROM users WHERE username LIKE ? ORDER BY username "+ user_preference, file=sys.stderr)

    r = db.execute(
        "SELECT name FROM users WHERE username LIKE ? ORDER BY username "
        + user_preference,
        [q],
    )

    friends = r.fetchall()
    num_friends = len(friends)
    friends_html = "".join([f"<li>{f[0]}</li>" for f in friends])

    return f"""
    <p> Found friends: {num_friends} </p>
    <ul>
        {friends_html}
    </ul>
    """


@app.route("/settings", methods=["GET", "POST"])
def settings():
    active_user = session.get("user")
    if not active_user:
        return redirect(url_for("login") + "?msg=Please+log+in")

    if request.method == "POST":
        new_ordering = request.form.get("order", "ASC")
        active_user["default_sort"] = new_ordering
        session["user"] = active_user
        return redirect(url_for("settings"))

    is_asc = session["user"]["default_sort"] == "ASC"

    return f"""
    <form method="post">
        <label>
            <input type="radio" name="order" value="ASC" {'checked' if is_asc else ''}> ASC
        </label><br>

        <label>
            <input type="radio" name="order" value="DESC" {'' if is_asc else 'checked'}> DESC
        </label><br>

        <button type="submit">Submit</button>
    </form>
    """


@app.route("/", methods=["GET", "POST"])
def home():
    active_user = session.get("user")
    if not active_user:
        return redirect(url_for("login"))
    msg = flash_msg()
    return f"""
        {msg}
        <h1>Welcome, {active_user['name']}</h1>

        <p>Try searching for your friends: <a href="/search">HERE</a>.</p>
        <p>Change your <a href="/settings">settings</a>.</p>
        """


@app.route("/login", methods=["GET", "POST"])
def login():
    active_user = session.get("user")
    if active_user:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return redirect(url_for("login"))

        db = get_db().cursor()
        r = db.execute(
            "SELECT username, password FROM users WHERE username = ?", [username]
        )
        user = r.fetchone()
        if not user:
            return redirect(url_for("login") + "?msg=Wrong+username+or+password")

        if not compare_password(user[1], password):
            return redirect(url_for("login") + "?msg=Wrong+username+or+password")

        session["user"] = init_session(username)
        return redirect(url_for("home"))
    msg = flash_msg()
    return f"""
    {msg}
    <form method="post">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username">
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password">
        </div>
        <div>
            <input type="submit" value="Login">
        </div>
    </form>
    """


@app.route("/best_friend")
def bestfriend():
    active_user = session.get("user")
    if not active_user:
        return redirect(url_for("login") + "?msg=Please+log+in")
    db = get_db().cursor()
    r = db.execute(
        "SELECT is_flagworthy FROM users WHERE username = ?", [active_user["username"]]
    )
    val = r.fetchone()
    worthy = val and val[0]
    if not worthy:
        return redirect(url_for("home") + "?msg=Guess+you+are+not+worthy")
    return f"""<pre>{FLAG}</pre>"""


@app.route("/register")
def register():
    return redirect(url_for("home") + "?msg=Not+Implemented")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login") + "?msg=Logged+out")


if __name__ == "__main__":
    app.run(port=5000)

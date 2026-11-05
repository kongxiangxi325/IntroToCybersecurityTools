import os
import sqlite3

from flask import Flask, jsonify, make_response, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "notes.db")

app = Flask(__name__)


def db():
    return sqlite3.connect(DB)


def init_db():
    conn = db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def page(name):
    return send_from_directory(os.path.join(BASE, "pages"), name)


@app.route("/")
def index():
    return page("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        return make_response(page("retry.html"), 400)
    conn = db()
    row = conn.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()
    if row is None:
        return make_response(page("retry.html"), 401)
    resp = make_response(page("home.html"), 200)
    resp.set_cookie("user", username)
    return resp


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        return make_response(page("retry.html"), 400)
    conn = db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return make_response(page("retry.html"), 409)
    conn.close()
    resp = make_response(page("home.html"), 201)
    resp.set_cookie("user", username)
    return resp


@app.route("/home")
def home():
    if request.cookies.get("user"):
        return page("home.html")
    return page("login.html")


@app.route("/me")
def me():
    username = request.cookies.get("user", "")
    return jsonify({"user": username})


@app.route("/logout")
def logout():
    resp = make_response(page("login.html"))
    resp.delete_cookie("user")
    return resp


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

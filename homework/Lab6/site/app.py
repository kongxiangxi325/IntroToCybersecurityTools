"""Lab6 教学站：注册、登录和当前身份查询。

仅限本机和课程虚拟机内网使用，禁止部署到公网。
教学简化：密码以明文保存，Cookie 直接保存用户名且没有签名。
"""

import os
import sqlite3

from flask import Flask, jsonify, make_response, request, send_from_directory

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "notes.db")
PAGES = os.path.join(BASE, "pages")


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "username TEXT UNIQUE NOT NULL,"
        "password TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()


def page(name):
    return send_from_directory(PAGES, name)


@app.route("/")
def index():
    return page("login.html")


@app.route("/home")
def home():
    if request.cookies.get("user", "") == "":
        return page("login.html")
    return page("home.html")


@app.route("/me")
def me():
    # TODO 7：把本注释和下一行 pass 换成两行代码：读取 Cookie 中的 user，再返回 JSON。
    pass


# TODO 3：给下面的函数补上路由声明：路径 /login，只接受 POST（写法见讲义 5.3 节）。
def login():
    username = request.form.get("username", "").strip()
    # TODO 4：仿照上一行写出读取 password 字段的语句：默认值为空字符串，密码不做 strip（见讲义 5.3 节）。

    if username == "" or password == "":
        return page("retry.html"), 400

    conn = db()
    row = conn.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()

    if row is None:
        return page("retry.html"), 401

    resp = make_response(page("home.html"))
    resp.set_cookie("user", username)
    return resp


# TODO 5：给下面的函数补上路由声明：路径 /register，只接受 POST（写法见讲义 5.4 节）。
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if username == "" or password == "":
        return page("retry.html"), 400

    conn = db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return page("retry.html"), 409
    finally:
        conn.close()

    resp = make_response(page("home.html"))
    resp.status_code = 201
    resp.set_cookie("user", username)
    return resp


@app.route("/logout")
def logout():
    resp = make_response(page("login.html"))
    resp.delete_cookie("user")
    return resp


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

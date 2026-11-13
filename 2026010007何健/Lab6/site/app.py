import os
import sqlite3

from flask import Flask, jsonify, make_response, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "notes.db")

app = Flask(__name__)


def db():
    """打开数据库文件，返回连接对象。"""
    conn = sqlite3.connect(DB)
    return conn


def init_db():
    """首次运行时建表；表已存在则跳过（IF NOT EXISTS）。"""
    conn = db()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );"""
    )
    conn.commit()
    conn.close()


def page(name):
    """把 pages/ 目录下的 HTML 文件作为响应返回。"""
    return send_from_directory(os.path.join(BASE, "pages"), name)


init_db()


@app.route("/")
def index():
    """GET /：返回登录页。"""
    return page("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    # 空字段检查在服务器端做，对一切客户端生效
    if username == "" or password == "":
        return make_response(page("retry.html"), 400)
    conn = db()
    row = conn.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()
    if row is None:
        # 密码错误：查不到记录，返回 401
        return make_response(page("retry.html"), 401)
    # 验证通过：返回成功页并设置 Cookie
    resp = make_response(page("home.html"), 200)
    resp.set_cookie("user", username)
    return resp


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if username == "" or password == "":
        return make_response(page("retry.html"), 400)
    conn = db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # 用户名重复（UNIQUE 约束），返回 409
        conn.close()
        return make_response(page("retry.html"), 409)
    conn.close()
    # 注册成功：201 已创建，并记录 Cookie
    resp = make_response(page("home.html"), 201)
    resp.set_cookie("user", username)
    return resp


@app.route("/home")
def home():
    """GET /home：读 Cookie，有值返回成功页，没值返回登录页。"""
    user = request.cookies.get("user", "")
    if user == "":
        return page("login.html")
    return page("home.html")


@app.route("/me")
def me():
    username = request.cookies.get("user", "")
    return jsonify({"user": username})


@app.route("/logout")
def logout():
    """GET /logout：删除 Cookie，返回登录页。"""
    resp = make_response(page("login.html"))
    resp.delete_cookie("user")
    return resp


if __name__ == "__main__":
    # 监听 0.0.0.0 以接受来自 Windows 宿主机的连接（实验最终态，见第八节）
    app.run(host="0.0.0.0", port=8000)

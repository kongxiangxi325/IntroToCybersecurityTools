# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800/flag.html |
| Flag | ctfhub{06e0e404e8d7c2f51ef95016} |

## 解题过程

按题目提示直接访问 `/flag.html`，第一次没有带任何凭据，服务器返回 `401 Unauthorized`，响应头里有 `WWW-Authenticate: Basic realm="..."` —— 这个响应头就是在告诉浏览器“这个资源要 Basic 认证”，于是浏览器弹出了用户名/密码输入框。我按题目页面给出的账号用 `admin`、密码用 `zxcvvbnm`，为了能把请求头完整留下来，改用 Kali 终端里的 `curl -u admin:zxcvvbnm` 重新请求：`-v` 打印出来可以看到，curl 自动把 `admin:zxcvvbnm` 拼起来做 Base64，生成的请求头是 `Authorization: Basic YWRtaW46enhjdnZibm0=`。服务器这次返回 `200 OK`、`Content-Type: text/html`、`Content-Length: 33`，响应体里就是 `ctfhub{06e0e404e8d7c2f51ef95016}`。回题目页面提交，通过。

## 关键请求/响应

```http
# 未认证：401 + WWW-Authenticate
GET /flag.html HTTP/1.1
Host: challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="CTFHub"

# 带上凭据后（curl -u admin:zxcvvbnm）
> GET /flag.html HTTP/1.1
> Host: challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800
> Authorization: Basic YWRtaW46enhjdnZibm0=
> User-Agent: curl/8.20.0

< HTTP/1.1 200 OK
< Server: openresty/1.21.4.2
< Date: Sat, 24 Oct 2026 13:01:11 GMT
< Content-Type: text/html; charset=utf-8
< Content-Length: 33

ctfhub{06e0e404e8d7c2f51ef95016}
```

## 原理与复盘

Base64 只是**编码**，不是加密：`YWRtaW46enhjdnZibm0=` 解出来就是明文的 `admin:zxcvvbnm`，任何人都能一秒还原，所以 `Authorization: Basic ...` 里装的本质是**明文用户名和密码**。它出现在请求头里，浏览器每次请求都带一遍；配合 401 + `WWW-Authenticate` 的挑战/应答流程虽然能用，但必须叠 HTTPS 才有意义，否则中间人抓到任何一个请求就拿到了密码。本题也说明：看到一串 Base64 别当成“加密后的密码”，先解开看看。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

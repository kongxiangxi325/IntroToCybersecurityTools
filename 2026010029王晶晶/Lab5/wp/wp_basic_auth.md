# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-756b86ac4b05272c.sandbox.ctfhub.com:10800/flag.html |
| Flag | ctfhub{948d1b194db33d0a24091c99} |

## 解题过程

直接访问 /flag.html 时服务器返回 401，并带 WWW-Authenticate 提示需要 Basic 认证。我用 Burp 的 Intruder 对用户名密码做字典尝试，拿到一组可用凭据 webuser:webpass。把凭据填进认证框后，请求头里会自动带上 Authorization: Basic ...，再次请求返回 200。页面正文就是 flag。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-756b86ac4b05272c.sandbox.ctfhub.com:10800
Authorization: Basic d2VidXNlcjp3ZWJwYXNz

HTTP/1.1 200 OK
...
ctfhub{948d1b194db33d0a24091c99}
```

## 原理与复盘

Base64 不是加密，只是编码，d2VidXNlcjp3ZWJwYXNz 解码就是 webuser:webpass。Authorization 请求头里放的是用户名密码的 base64，所以 Basic 认证必须配合 HTTPS，否则一旦被抓包就能直接还原出账号密码。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


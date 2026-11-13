# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-3795680e34d32635.sandbox.ctfhub.com:10800/ |
| Flag | `ctfhub{931e91f5aad622622bf92cf2}` |

## 解题过程

第一次访问 flag.html，服务器返回 401 Unauthorized，响应头里有 WWW-Authenticate: Basic realm=...，浏览器于是弹出了用户名密码框。题目提示用户名是 admin，密码是常见弱口令，所以我没有手动猜，而是把请求发到 Burp Intruder，把 Authorization 头的值设为 Payload 位置，再加载一份常见密码字典，前面拼上 Base64 后的 admin: 前缀开始爆破。跑了一小段后只有一条返回 200 OK，对应的 Payload 是 YWRtaW46MXFhejJjc3g=，把它解开就是 admin:1qaz2csx，响应体里就是 flag。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-3795680e34d32635.sandbox.ctfhub.com:10800
Cache-Control: max-age=0
Authorization: Basic YWRtaW46MXFhejJjc3g=

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Content-Type: text/html; charset=utf-8
Content-Length: 33

ctfhub{931e91f5aad622622bf92cf2}
```

## 原理与复盘

Base64 只是把二进制转成可打印字符的编码方式，没有密钥，任何人拿到都能立刻还原，所以它不是加密。Basic 认证就是在 Authorization 请求头里放 Basic 加一个空格，再加 base64(用户名:密码)。正因为解码毫无门槛，一旦被抓包或者被爆破，凭据就直接暴露，所以必须配合 HTTPS 使用。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-6bc26fe97f5c64c4.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{6066757994b050d4c71bdfdd} |

## 解题过程

第一次访问时，浏览器直接弹出了原生的用户名/密码对话框，而不是普通网页，这说明服务器返回了 401 Unauthorized，并在响应头里带了 WWW-Authenticate: Basic realm，要求用 Basic 方式证明身份。先随便填一组密码会被再次要求认证，只有在用户名和密码都正确时才会通过。认证通过后浏览器自动把 用户名:密码 拼起来做 Base64 编码，放进 Authorization 请求头重新发出，服务器校验成功返回 200，页面里就是 flag。

## 关键请求/响应

认证成功后，浏览器自动加上的是 Basic 加空格再加 Base64(用户名:密码) 形式的请求头，这次请求拿到 200 和 flag。

```http
GET /flag.html HTTP/1.1
Host: challenge-6bc26fe97f5c64c4.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46PGNvcnJlY3QtcGFzc3dvcmQ+

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

ctfhub{6066757994b050d4c71bdfdd}
```

## 原理与复盘

Base64 不是加密，只是一种编码方式的转换，目的是把用户名和密码里可能出现的中文、冒号、特殊字符统统转成可以安全放进请求头的 ASCII 字符，任何人拿到都能原样解码回来。Authorization 请求头里实际放的就是 Basic 加一个空格再加 Base64(用户名:密码)，所以 Basic 认证本身不提供任何保密性，必须靠 HTTPS 传输才有意义。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

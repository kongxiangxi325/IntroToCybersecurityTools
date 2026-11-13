# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-36f9e54e1e9a342b.sandbox.ctfhub.com:10800/flag.html |
| Flag | ctfhub{5fd46716613c19936727654} |

## 解题过程

第一次访问 flag.html 时浏览器弹出了用户名密码框，用 Burp 抓包能看到服务器返回的是 `401 Unauthorized`，响应头里有 `WWW-Authenticate: Basic realm="..."`，说明这是 HTTP Basic 认证。题目页面还提供了一个常用密码字典附件，我下载后决定用 Burp Intruder 爆破：把请求发到 Intruder，对 `Authorization` 头中 `Basic ` 后面的 Base64 段做替换，payload 是把用户名 `admin:` 和字典里每个密码拼接后再 Base64 编码的结果。跑完后按状态码排序，全部 401 中只有一个 200 的请求，它的 Authorization 头是 `Basic YWRtaW46YWtzbWhlYg==`（Base64 解码后是 `admin:aksmheb`），对应的响应体里就是 flag，提交成功。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-36f9e54e1e9a342b.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46YWtzbWhlYg==

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

ctfhub{5fd46716613c19936727654}
```

（爆破失败时该请求均为 `HTTP/1.1 401 Unauthorized`，响应长度 81 字节；唯一的 200 请求响应长度 383 字节。）

## 原理与复盘

这道题对应 HTTP 报文的请求头和响应头：401 响应用 `WWW-Authenticate: Basic` 告诉客户端“需要 Basic 认证”，客户端则把 `用户名:密码` 做 Base64 编码放进 `Authorization` 请求头重发。Base64 只是编码、不是加密，任何人拿到 `YWRtaW46YWtzbWhlYg==` 都能立刻还原出 `admin:aksmheb`，所以 Basic 认证必须配合 HTTPS 使用，否则等于明文传密码。另外本题的密码在常用字典里，说明弱口令是 Basic 认证最大的软肋，服务端应做失败次数限制。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

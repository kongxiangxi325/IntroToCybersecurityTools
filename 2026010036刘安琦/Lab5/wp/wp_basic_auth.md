# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-5ec3c1f4b474a708.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{314c452fffd0cb7dc820e89d} |

## 解题过程

访问环境时，服务器返回了 `401 Unauthorized`，说明需要认证，响应头里有 `WWW-Authenticate: Basic`，提示这是 HTTP Basic 认证。题目又暗示用户名可能和 "admin" 有关。我用 Burp 的 Intruder，把 `Authorization` 请求头里的值作为爆破位置，对密码部分做字典爆破，最终爆破出一个返回 200 的请求。用这个认证凭据重新访问，就拿到了 flag。

## 关键请求/响应

爆破成功后带上认证头的请求：

```http
GET / HTTP/1.1
Host: challenge-5ec3c1f4b474a708.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46bGV0bWVpbg==
```

其中 `YWRtaW46bGV0bWVpbg==` 是 `admin:letmein` 的 Base64 编码。响应返回 200，响应体为 flag：

```
ctfhub{314c452fffd0cb7dc820e89d}
```

## 原理与复盘

HTTP Basic 认证的做法是：客户端把 `用户名:密码` 拼起来做 Base64 编码，放进 `Authorization: Basic <编码>` 请求头里发给服务器。注意 Base64 只是编码、不是加密，任何人拿到这串字符都能直接解码还原出明文密码。本题凭据可被字典爆破出来，也说明了弱口令 + 明文可还原的认证方式很不安全。对应到 HTTP 报文，这考查的是请求头里的 `Authorization` 字段。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

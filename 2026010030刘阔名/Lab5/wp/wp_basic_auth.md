# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-038859a5a0c851e.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{966a303508ea4461bf09bf4e} |

## 解题过程

开启题目后访问靶场首页，服务器返回 `401 Unauthorized`，响应头中带 `WWW-Authenticate: Basic realm="..."`，浏览器弹出用户名/密码登录框，说明这是 HTTP Basic 认证。题目提示是弱口令，并且页面提供了「加密访问」选项——勾选后前端会把密码加密再提交。我在 Burp 中把登录请求发送到 Intruder，username 固定为 `admin`，把 `password` 的值设为 payload 位置，用常见弱口令字典逐个尝试。抓到的请求体里，password 是加密后的密文；当密文为 `021256` 时返回 `200 OK`，响应体中直接出现了 flag，它对应的明文密码是 `696969`。请求头中的 `Authorization: Basic YWRtaW46YWRtaW4=`（解码为 `admin:admin`）则体现了 Basic 认证把凭证做 Base64 后放进请求头的方式。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-038859a5a0c851e.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46YWRtaW4=
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

username=admin&password=021256

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Content-Type: text/html; charset=UTF-8
X-Powered-By: PHP/5.6.40

ctfhub{966a303508ea4461bf09bf4e}
```

> 说明：请求体中的 `password=021256` 是明文密码 `696969` 在开启「加密访问」后提交的密文。

## 原理与复盘

这道题对应 HTTP 报文的 **请求头 Authorization**。Basic 认证只是把 `用户名:密码` 用 Base64 编码后放在请求头里传输；Base64 不是加密，只是编码，任何人拿到后都能解码还原出原始明文。因此弱口令 + Basic 认证非常危险，攻击者一旦截获请求或直接猜测密码就能绕过认证。

---

## 截图

![基础认证](https://raw.githubusercontent.com/liukuoming/IntroToCybersecurityTools/lab5-submit/2026010030%E5%88%98%E9%98%94%E5%90%8D/Lab5/imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

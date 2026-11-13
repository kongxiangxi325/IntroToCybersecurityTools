# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 |http://challenge-756b86ca4b05272c.sandbox.ctfhub.com:10800/  |
| Flag | ctfhub{948d1b194db33d0a24091c99} |

## 解题过程

第一次访问时浏览器直接弹出用户名和密码输入框，随便填一个，Burp 里看到返回的是 401 Unauthorized 和 WWW-Authenticate: Basic realm=... 响应头，说明这是 HTTP Basic 认证。题目页面提示用户名是 admin，我用 MobaXterm 把密码字典从 Windows 传进 Kali，在 Burp 里把请求发送到 Intruder，把 Authorization 头里 Basic 后面那段 Base64 设成爆破点，并在 Payload processing 里加一条对 admin:字典项 做 Base64 编码的规则，加载字典后开始攻击。结果里按 Length 排序，发现有一条响应的长度和其他请求明显不同，点开看 payload 是 696969，解码后就是 admin:696969。认证通过后服务器不再返回 401，而是把 flag 放在 /flag.html 这个页面里返回，我把这条请求发送到 Repeater 重放，响应体里就是 ctfhub{948d1b194db33d0a24091c99}，回到题目页面提交后提示正确。

## 关键请求/响应

```http
请求包：
GET /flag.html HTTP/1.1
Host: challenge-756b86ca4b05272c.sandbox.ctfhub.com:10800
Cache-Control: max-age=0
Authorization: Basic YWRtaW46Njk2OTY5
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
响应包:
HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Fri, 23 Oct 2026 02:22:40 GMT
Content-Type: text/html; charset=utf-8
Connection: keep-alive
Last-Modified: Fri, 23 Oct 2026 01:53:44 GMT
ETag: W/"6adabe28-21"
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 33
ctfhub{948d1b194db33d0a24091c99}

```

## 原理与复盘

Base64 只是一种编码方式，不是加密，Authorization 头里放的就是 `用户名:密码` 做 Base64 之后的结果，把 YWRtaW46Njk2OTY5 解出来就是 admin:696969。正因为只是编码，密码字典可以批量编码后直接塞进请求头，服务端返回的状态码和响应长度就会告诉攻击者哪个密码对了，Basic 认证本身几乎没有防爆破能力。另外它在 HTTP 下是明文传输的，必须配合 HTTPS 才有意义。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


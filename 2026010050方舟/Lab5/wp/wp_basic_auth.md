# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-1eeeff168407239b.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{3525f0c0be5be4e261ad0527} |

## 解题过程

第一次访问靶场地址，浏览器弹出用户名/密码输入框；如果点取消，返回的就是 `HTTP/1.1 401 Unauthorized`，响应头里带 `WWW-Authenticate: Basic realm="..."`，这说明服务器要的是 HTTP Basic 认证，而且密码得自己想办法。题目给的用户名是 `admin`，于是我把浏览器挂到 Burp，抓到 `GET /flag.html` 这条请求，Send to Intruder，在 Positions 里把 `Authorization: Basic §payload§` 这一段的原值替换成载荷位置，Payloads 选一组常见密码字典，Payload processing 里加两条规则：先加前缀 `admin:`，再对整体做 Base64 编码（这就是自动拼出 `admin:密码` 再编码）。开始攻击后，结果列表里绝大多数请求都是 401，只有一条 Status code 是 200，对应密码 `austin`，Base64 是 `YWRtaW46YXVzdGlu`。看这条的 Response，正文就是 `ctfhub{3525f0c0be5be4e261ad0527}`，回平台提交正确。最后我把这条成功的请求在 Repeater 里单独重放一次，确认 `Authorization: Basic YWRtaW46YXVzdGlu` 就是唯一有效的凭证，顺便截图。

## 关键请求/响应

Intruder 第 98 条（唯一 200）的请求与响应，同时在 Repeater 里重放确认过：

```http
GET /flag.html HTTP/1.1
Host: challenge-1eeeff168407239b.sandbox.ctfhub.com:10800
Cache-Control: max-age=0
Authorization: Basic YWRtaW46YXVzdGlu
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Referer: http://challenge-1eeeff168407239b.sandbox.ctfhub.com:10800/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 17:55:24 GMT
Content-Type: text/html; charset=utf-8
Connection: keep-alive
Last-Modified: Sat, 24 Oct 2026 17:29:08 GMT
ETag: W/"6adceae4-21"
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 33

ctfhub{3525f0c0be5be4e261ad0527}
```

`YWRtaW46YXVzdGlu` 解码就是 `admin:austin`；认证失败的那一条则是 `401 Unauthorized` + `WWW-Authenticate: Basic`。

## 原理与复盘

Basic 认证在报文上的位置是**请求头** `Authorization: Basic <Base64>`，括号里是 `用户名:密码` 拼起来再 Base64 编码的结果；它不是加密，因为 Base64 只是可逆的字符替换，`base64 -d` 一秒就还原。失败时服务器用 401 + `WWW-Authenticate: Basic` 提示浏览器弹出登录框，浏览器拿到用户名密码后再把这个头自动加上重发。所以这道题的“爆破”本质是把客户端必须提交的那一行猜出来：用户名已知、密码是弱口令，编码规则固定，Intruder 挂字典就能筛出唯一 200。真正的教训是——Basic 认证必须配 HTTPS，否则用户名密码在网线里就是明文；以及别指望“编码过”就等于安全。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

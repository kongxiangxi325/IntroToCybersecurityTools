# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-db094d2dc2c8ec04.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{3eee77bda7a3c4dab271fa3e} |

## 解题过程

首页写着「Here is your flag: click」，点过去访问 `/flag.html` 时浏览器弹出登录框。我用 `curl -si` 直接请求 `/flag.html`，拿到 `401 Unauthorized` 和 `WWW-Authenticate: Basic realm="Do u know admin ?"`——realm 里的这句话基本就是在提示用户名是 `admin`。题目附件给的是 `10_million_password_list_top_100` 密码本，说明密码要在这 100 个里挑，于是我在 Kali 里写了个小脚本，把 `admin:` 和字典词拼起来做 Base64 再丢进 `Authorization` 头逐个试，最后 `admin:klaster` 返回 200，页面给出 flag。截图里同时保留了 401+WWW-Authenticate 和 200 成功两次请求，能看清 `-u admin:klaster` 这个凭据。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-db094d2dc2c8ec04.sandbox.ctfhub.com:10800
User-Agent: curl/8.5.0

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Do u know admin ?"
Content-Type: text/html; charset=utf-8

GET /flag.html HTTP/1.1
Host: challenge-db094d2dc2c8ec04.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46a2xhc3Rlcg==      （Base64 解码后是 admin:klaster）
User-Agent: curl/8.5.0

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 33

ctfhub{3eee77bda7a3c4dab271fa3e}
```

## 原理与复盘

Base64 只是**编码**不是加密，任何人都能秒解码，所以 Basic 认证本质上等于把 `用户名:密码` 用明文（只是换了个字符集）在 HTTP 请求头 `Authorization` 里传。这题把凭据放在**请求头**，服务器返回 401 时用 `WWW-Authenticate` 告诉客户端"请用 Basic 方式提供凭据"，于是就能按字典爆破。现实中 Basic 认证必须配 HTTPS，否则中间人抓一个包就能还原出账号密码。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

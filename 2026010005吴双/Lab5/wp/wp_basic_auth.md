# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-f921cb1ec6270a81.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{db4121aebfcf5f8d0f467264} |

## 解题过程

靶场首页写着 `Here is your flag: <a href="/flag.html">click</a>`，但点进去直接返回 `401 Unauthorized`，响应头里带着 `WWW-Authenticate: Basic realm="Do u know admin ?"`。这个响应头既说明它用的是 HTTP Basic 认证，也顺便把用户名透露了——realm 里点名 admin。

用户名有了，密码不知道，于是我在 Kali 里用 rockyou 字典的前 3000 条做小规模尝试：对每个候选密码拼成 `admin:口令`，Base64 之后放进 `Authorization: Basic ...` 请求头，并发请求 `/flag.html`，只要返回 200 且正文里有 `ctfhub{` 就停下。字典跑到 `charlie` 时命中，随后用 `curl -u admin:charlie` 再请求一次，确认状态码变成 200，正文就是 flag。

这一题不需要改浏览器设置，`curl -u` 会自动把用户名密码编码成 `Authorization` 头，和浏览器弹出登录框后手动输入是等效的。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-f921cb1ec6270a81.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46Y2hhcmxpZQ==

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Content-Type: text/html; charset=utf-8
Content-Length: 33

ctfhub{db4121aebfcf5f8d0f467264}
```

（对照：不带头时返回 `HTTP/1.1 401 Unauthorized` + `WWW-Authenticate: Basic realm="Do u know admin ?"`）

## 原理与复盘

Base64 只是编码，不是加密：`YWRtaW46Y2hhcmxpZQ==` 解出来就是明文的 `admin:charlie`，任何人都能还原，所以 Basic 认证必须跑在 HTTPS 上，否则等于明文传密码。`Authorization` 头里放的就是 `Basic ` 加上 `用户名:密码` 的 Base64，服务器解码后比对；401 配合 `WWW-Authenticate` 是服务端“要求认证”的标准握手方式。这题也说明弱口令是真实风险，字典一小段就能撞开。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

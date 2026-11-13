# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-1c013689c190aba7.sandbox.ctfhub.com:10800/flag.html |
| Flag | ctfhub{f7935b48bb4513f8c0f99bc8} |

## 解题过程

首页只有一句 Here is your flag 和一个指向 /flag.html 的链接，点进去却没有页面，直接弹出用户名密码对话框，说明这个文件被 HTTP Basic 认证保护着。用 curl -i 看原始响应，返回 401 Unauthorized，响应头里是 WWW-Authenticate: Basic realm="Do u know admin ?"，题目等于直接告诉我用户名是 admin，密码要自己猜。题目附件给了一份 10_million_password_list_top_100.txt 常用密码字典，于是写了一个 while 循环，用 curl -u admin:密码 逐条请求 /flag.html，只取状态码，遇到 200 就停。第 20 条左右命中 admin:mustang，再带上这组账号访问，返回 200 和 flag。最后确认一下请求头，Authorization 的值是 admin:mustang 做过 Base64 之后的 YWRtaW46bXVzdGFuZw==。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-1c013689c190aba7.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46bXVzdGFuZw==
User-Agent: curl/8.20.0
Accept: */*

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 33

ctfhub{f7935b48bb4513f8c0f99bc8}
```

不带 Authorization 头时返回 401 与 WWW-Authenticate: Basic realm="Do u know admin ?"；带上 admin:mustang 的 Base64 值后返回 200 和 flag。

## 原理与复盘

Base64 只是一种编码，不是加密：它没有密钥，任何人都能一眼解回原文，YWRtaW46bXVzdGFuZw== 解出来就是 admin:mustang。Authorization: Basic 请求头里放的实际是“用户名:密码”这段明文的 Base64 编码，所以 Basic 认证必须跑在 HTTPS 上，否则等于把密码裸奔在网络上；同时密码强度也要够，本题能被 100 条常用密码字典打穿就是反面例子。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

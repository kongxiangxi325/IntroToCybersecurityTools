# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-d2a773085010ad72.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{f3cb2f797dcdd1924c8c928e} |

## 解题过程

靶场首页写着「Here is your flag: click」，链接指向 `/flag.html`。直接访问 `/flag.html` 返回 `401 Unauthorized`，响应头里有 `WWW-Authenticate: Basic realm="Do u know admin ?"`，说明这个页面要走 HTTP Basic 认证。题目同时给了一个密码字典压缩包（`10_million_password_list_top_100.txt`，100 个常见密码），用户名从 realm 提示看就是 `admin`。我 `curl -u admin:密码` 写了个 `while read` 循环把字典跑了一遍，前几个都没过，跑到 `michelle` 时状态码从 401 变成 200，页面返回 `ctfhub{f3cb2f797dcdd1924c8c928e}`。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-d2a773085010ad72.sandbox.ctfhub.com:10800

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Do u know admin ?"
------------------------------
GET /flag.html HTTP/1.1
Host: challenge-d2a773085010ad72.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46bWljaGVsbGU=

HTTP/1.1 200 OK

ctfhub{f3cb2f797dcdd1924c8c928e}
```

## 原理与复盘

Basic 认证把 `用户名:密码` 用 Base64 编码后放进 **`Authorization` 请求头**，本题里 `admin:michelle` 编码后就是 `YWRtaW46bWljaGVsbGU=`。Base64 是编码不是加密，任何人拿到这串都能一秒解回明文，所以 Basic 认证必须配 HTTPS 使用；同时密码强度才是真正的防线，字典里的常见密码几秒就被跑穿了。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


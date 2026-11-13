# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-1bf5f8b447d58efd.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{8946ebdd2f92e9a2bc468551} |

## 解题过程

打开题目首页，页面很简单，只有一句提示和一个指向 /flag.html 的链接。点这个链接时浏览器直接弹出原生的用户名密码对话框，说明服务器返回了 401，响应头里带着 WWW-Authenticate: Basic realm="Do u know admin ?"，没有登录就进不去。

realm 里写了 admin，说明用户名就是 admin，接下来只剩密码。这种没有验证码、也没有次数限制的认证，最省事的办法就是拿常见弱口令挨个试。我在 Kali 里用 curl 带着 -u admin:密码 一条条发过去，看返回码从 401 变成 200 就是试对了；试到 iloveyou 时返回 200，页面正文里就是 flag。

于是把 admin:iloveyou 按 用户名:密码 拼起来做 Base64，得到 YWRtaW46aWxvdmV5b3U=，再用 curl -v 发一次，请求头里能看到 Authorization: Basic 这一行，响应 200，正文返回 flag。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-1bf5f8b447d58efd.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46aWxvdmV5b3U=
User-Agent: curl/8.20.0

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Content-Type: text/html; charset=utf-8

ctfhub{8946ebdd2f92e9a2bc468551}
```

## 原理与复盘

Base64 不是加密，只是一种编码方式的转换，目的是把用户名和密码里可能出现的中文、冒号、特殊字符统统转成可以安全放进请求头的 ASCII 字符，任何人拿到都能原样解码回来。Authorization 请求头里实际放的就是 Basic 加一个空格再加 Base64(用户名:密码)，所以 Basic 认证本身不提供任何保密性，必须靠 HTTPS 传输才有意义。

这道题真正暴露的问题是口令强度：admin 这种默认账号配上 iloveyou 这种字典里排得很靠前的密码，谁都能登进来，而且服务器连失败次数都不限制，等于把爆破的门槛降到零。实际部署里至少要换成强口令、限制失败次数，并且全程走 HTTPS。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

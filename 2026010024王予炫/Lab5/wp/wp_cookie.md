# WP：Cookie

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → Cookie
> **任务**：按题目提示修改 Cookie，拿到 flag。
> **提示**：在 DevTools 的 Application/Storage → Cookies 中查看 Cookie，或在 Burp 的请求头中查看。修改后重放请求，观察页面变化。
> **截图要求**：能看到修改后的 Cookie 请求头，以及服务器返回的 flag 或成功页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-bc1819b0ed9e1b41.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{995e543be2dacc5d2098cb42} |

## 解题过程

第一次访问靶场首页时，页面显示 `hello guest. only admin can get flag.`，身份是 guest。打开 DevTools 的 Application → Cookies 一看，服务器在响应头里下发了一个 `Set-Cookie: admin=0`，浏览器之后每次请求都会自动把它放进请求头的 `Cookie` 里。这说明身份不是靠登录态判断，而是直接取决于 `admin` 这个 Cookie 的值，于是我把它的值从 `0` 改成 `1`。为了确认能稳定复现，我又在 Kali 终端用 `curl -b "admin=1"` 重发了一次同一个请求，服务器返回 `200 OK`，响应体里直接给出 `ctfhub{995e543be2dacc5d2098cb42}`。回题目页面提交，通过。

## 关键请求/响应

```http
# 第一次访问：服务器下发身份
GET / HTTP/1.1
Host: challenge-bc1819b0ed9e1b41.sandbox.ctfhub.com:10800

HTTP/1.1 200 OK
Set-Cookie: admin=0
Content-Type: text/html; charset=UTF-8

hello guest. only admin can get flag.

# 修改 Cookie 后重放
GET / HTTP/1.1
Host: challenge-bc1819b0ed9e1b41.sandbox.ctfhub.com:10800
Cookie: admin=1

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 13:34:20 GMT
Content-Type: text/html; charset=UTF-8
X-Powered-By: PHP/5.6.40

ctfhub{995e543be2dacc5d2098cb42}
```

## 原理与复盘

Cookie 是**请求头**里的一行 `Cookie: name=value`，服务器先用响应头 `Set-Cookie` 把它种到客户端，之后浏览器每次请求都自动带回来，服务器就靠它认出“这是谁”，所以它是一个完全由客户端保管、客户端能改的状态。本题把权限直接写成了 `admin=0/1`，改个数字就成了管理员 —— 也就是说，凡是权限判断只依赖 Cookie 里的明文值（哪怕做了 Base64 或简单编码），都等于把权限交给了用户。正确做法是把身份放在服务端 Session 里，Cookie 只存一个不可预测的 SessionID，服务端自己判断这个 Session 是不是管理员。

---

## 截图

![Cookie](../imgs/lab5_cookie.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

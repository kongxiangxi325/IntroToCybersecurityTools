# WP：Cookie

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → Cookie
> **任务**：按题目提示修改 Cookie，拿到 flag。
> **提示**：在 DevTools 的 Application/Storage → Cookies 中查看 Cookie，或在 Burp 的请求头中查看。修改后重放请求，观察页面变化。
> **截图要求**：能看到修改后的 Cookie 请求头，以及服务器返回的 flag 或成功页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-a3f5a42d12ca53.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{562beea6169241eae130ffa0} |

## 解题过程

首页显示“hello guest, only admin can get flag.”，说明服务器把当前身份当成了 guest。抓包后发现请求头里带了一个 Cookie，服务端就是靠它判断身份。我把 Cookie 的值改成 admin=1 后重放请求，页面不再显示 guest，响应体里直接给出了 flag。

## 关键请求/响应

```http
GET / HTTP/1.1
Host: challenge-a3f5a42d12ca53.sandbox.ctfhub.com:10800
Cookie: admin=1

HTTP/1.1 200 OK
...
ctfhub{562beea6169241eae130ffa0}
```

## 原理与复盘

Cookie 放在请求头里，浏览器每次请求都会自动带上。如果服务端只凭 Cookie 的值判断身份、不做签名或会话校验，客户端就能随手改，属于典型的信任客户端输入的问题。

---

## 截图

![Cookie](../imgs/lab5_cookie.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


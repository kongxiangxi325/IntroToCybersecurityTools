# WP：Cookie

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → Cookie
> **任务**：按题目提示修改 Cookie，拿到 flag。
> **提示**：在 DevTools 的 Application/Storage → Cookies 中查看 Cookie，或在 Burp 的请求头中查看。修改后重放请求，观察页面变化。
> **截图要求**：能看到修改后的 Cookie 请求头，以及服务器返回的 flag 或成功页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-b9f4c3fa69af689d.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{6f48b9706574da4243063d7b} |

## 解题过程

打开靶场首页后，页面提示只有 `admin` 才能看到 flag。我按 `F12` 打开浏览器 DevTools，切换到 Application/Storage → Cookies，看到当前域名下有一个名为 `admin` 的 Cookie，值是 `0`。把它的值改成 `1` 后刷新页面，页面内容发生变化，直接显示出了 flag。为了留下可复查的证据，我又把请求发到 Burp Repeater，在请求头里加上 `Cookie: admin=1` 重放，服务器返回 `200 OK`，响应体中就是同一个 flag。

## 关键请求/响应

```http
GET / HTTP/1.1
Host: challenge-b9f4c3fa69af689d.sandbox.ctfhub.com:10800
Cookie: admin=1

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

ctfhub{6f48b9706574da4243063d7b}
```

## 原理与复盘

这道题对应 HTTP 报文的 **请求头 Cookie**。Cookie 存储在客户端，由浏览器随请求自动发送给服务器。服务器如果仅用 Cookie 中的某个字段（如 `admin=0/1`）来判断用户权限，攻击者就可以通过篡改 Cookie 伪造身份。这说明敏感权限判断不能单独依赖客户端可控的数据。

---

## 截图

![Cookie](../imgs/lab5_cookie.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

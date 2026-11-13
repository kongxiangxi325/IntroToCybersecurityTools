# WP：Cookie

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → Cookie
> **任务**：按题目提示修改 Cookie，拿到 flag。
> **提示**：在 DevTools 的 Application/Storage → Cookies 中查看 Cookie，或在 Burp 的请求头中查看。修改后重放请求，观察页面变化。
> **截图要求**：能看到修改后的 Cookie 请求头，以及服务器返回的 flag 或成功页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-cf2d1005accf1372.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{177798d50aa5bf3e98e4753c} |

## 解题过程

浏览器打开靶场首页，页面只说自己不是 admin，拿不到 flag，但地址栏和页面上没有任何提示该改哪里。我把浏览器挂到 Burp 代理后刷新页面，在 HTTP history 里看这条 `GET / HTTP/1.1` 请求，请求头最后一行是 `Cookie: ...`，值是服务器下发的普通身份标识，不是 `admin=1`。我把它 Send to Repeater，把整个 Cookie 头的值直接改成 `admin=1`，再点 Send。响应从原来的普通页面变成了 `ctfhub{177798d50aa5bf3e98e4753c}`，说明服务器只凭这个 Cookie 值判断我是不是管理员。改完之后我又在 DevTools 的 Application → Cookies 里对着看了一眼，确认浏览器实际发出去的就是 `admin=1`，两边一致。

## 关键请求/响应

```http
GET / HTTP/1.1
Host: challenge-cf2d1005accf1372.sandbox.ctfhub.com:10800
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Cookie: admin=1

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Content-Type: text/html; charset=utf-8
Connection: keep-alive
Access-Control-Allow-Origin: *
Content-Length: 32

ctfhub{177798d50aa5bf3e98e4753c}
```

修改前的请求头里 Cookie 的值是普通用户标识（不是 `admin=1`），改成 `admin=1` 后服务器返回 200 和 flag。

## 原理与复盘

Cookie 放在**请求头**里，由浏览器自动带上、发给服务器；服务器读这个字段来“认人”，再决定给什么权限。问题在于 Cookie 完全存在客户端，用户想改成什么就改成什么，Burp、DevTools、甚至地址栏里写 JS 都能改，所以它只能当“身份的携带凭证”，不能当“身份本身”。只要服务端拿 Cookie 里的 `admin=1` 直接信了，就等于把权限判断交给了攻击者——这也是为什么真实系统里要用服务端 Session 或签名过的 Token，并且每次都在服务端重新校验权限。

---

## 截图

![Cookie](../imgs/lab5_cookie.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

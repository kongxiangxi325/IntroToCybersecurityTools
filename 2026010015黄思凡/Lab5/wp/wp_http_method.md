# WP：请求方式

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 请求方式
> **任务**：按题目要求使用指定的 HTTP 方法访问目标，拿到 flag。
> **提示**：浏览器地址栏默认发送 GET 请求。用 Burp Repeater 修改请求行中的方法，或者用 `curl -X` 复现。
> **截图要求**：优先使用 Burp Repeater，截图中要能看到修改后的请求行（方法 + 路径）和响应中的 flag；如果 Burp 无法启动，可以用 `curl -X` 的方法修改截图代替，并在 WP 中说明原因。只有浏览器普通 GET 访问不算完成。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-416307d3d1399c99.sandbox.ctfhub.com:10800/index.php |
| Flag |   ctfhub{8c13107b8cf1e51c40ba2109}|

## 解题过程

发现网页请求要求是get,在burpsuite里将其发送到repeat后修改为CTFHUB后发送，在响应包中发现flag

## 关键请求/响应

```http
请求包
CTFHUB /index.php HTTP/1.1
Host: challenge-416307d3d1399c99.sandbox.ctfhub.com:10800
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Referer: http://challenge-416307d3d1399c99.sandbox.ctfhub.com:10800/index.php
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
响应包
HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Fri, 23 Oct 2026 11:51:25 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/5.6.40
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 172
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <title>CTFHub HTTP Method</title>
</head>
<body>
good job! ctfhub{8c13107b8cf1e51c40ba2109}
</body>
</html>

```

## 原理与复盘

HTTP请求行由请求方法，请求路径，HTTP协议版本三部分构成。请求方法在请求行的最开头

---

## 截图

![请求方式](../imgs/lab5_http_method.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


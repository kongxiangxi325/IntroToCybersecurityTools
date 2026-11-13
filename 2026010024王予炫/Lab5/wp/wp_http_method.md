# WP：请求方式

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 请求方式
> **任务**：按题目要求使用指定的 HTTP 方法访问目标，拿到 flag。
> **提示**：浏览器地址栏默认发送 GET 请求。用 Burp Repeater 修改请求行中的方法，或者用 `curl -X` 复现。
> **截图要求**：优先使用 Burp Repeater，截图中要能看到修改后的请求行（方法 + 路径）和响应中的 flag；如果 Burp 无法启动，可以用 `curl -X` 的方法修改截图代替，并在 WP 中说明原因。只有浏览器普通 GET 访问不算完成。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-68948bbecb4c9ab6.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{68b8d6b24112459d9efba13c} |

## 解题过程

用浏览器打开靶场首页时，服务端只返回一句提示，大意是“当前请求用的不是题目要求的方法”，把要用的方法名点明了 —— 要用 `CTFHUB` 这个方法访问 `/index.php`，而不是浏览器地址栏默认的 `GET`。我先试了在 Burp 里抓这个请求，但 Kali 里的 Firefox 没有走 `127.0.0.1:8080` 代理，HTTP history 里一直是空的，按模板允许的替代方案改用 Kali 终端里的 `curl -v` 复现。命令是 `curl -v -X CTFHUB http://challenge-68948bbecb4c9ab6.sandbox.ctfhub.com:10800/index.php`，`-v` 会把发出去的报文原样打印，所以请求行写成了 `CTFHUB /index.php HTTP/1.1`，方法被换掉、路径和版本没变。服务器返回 `200 OK`，响应体是 `<title>CTFHub HTTP Method</title>` 加一行 `good job! ctfhub{68b8d6b24112459d9efba13c}`。回题目页面提交 flag，通过。

## 关键请求/响应

```http
> CTFHUB /index.php HTTP/1.1
> Host: challenge-68948bbecb4c9ab6.sandbox.ctfhub.com:10800
> User-Agent: curl/8.20.0
> Accept: */*

< HTTP/1.1 200 OK
< Server: openresty/1.21.4.2
< Date: Fri, 23 Oct 2026 09:04:53 GMT
< Content-Type: text/html; charset=UTF-8
< Connection: keep-alive
< X-Powered-By: PHP/5.6.40

<html>
<head>
  <meta charset="UTF-8">
  <title>CTFHub HTTP Method</title>
</head>
<body>
  good job! ctfhub{68b8d6b24112459d9efba13c}
</body>
</html>
```

## 原理与复盘

请求行由三部分组成：**方法** + **请求 URI** + **HTTP 版本**，中间用空格分隔，所以方法永远是这一行的第一个词；把 `GET` 换成 `CTFHUB`，路径 `index.php` 和版本 `HTTP/1.1` 都不用动，服务器就会按另一套逻辑处理同一个资源。HTTP 方法本来是可扩展的，服务端可以自己定义 `CTFHUB` 这样的方法，本题就是靠这个方法名区分“普通浏览”和“拿到 flag 的请求”。对防守方来说这也说明：只按 URL 做访问控制是不够的，方法、请求头都可能成为绕过点。

---

## 截图

![请求方式](../imgs/lab5_http_method.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

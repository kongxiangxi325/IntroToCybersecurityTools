# WP：请求方式

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 请求方式
> **任务**：按题目要求使用指定的 HTTP 方法访问目标，拿到 flag。
> **提示**：浏览器地址栏默认发送 GET 请求。用 Burp Repeater 修改请求行中的方法，或者用 `curl -X` 复现。
> **截图要求**：优先使用 Burp Repeater，截图中要能看到修改后的请求行（方法 + 路径）和响应中的 flag；如果 Burp 无法启动，可以用 `curl -X` 的方法修改截图代替，并在 WP 中说明原因。只有浏览器普通 GET 访问不算完成。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-416307d3f399d99.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{8c13107b8cf1e51c40ba2109} |

## 解题过程

打开页面后看到提示“HTTP Method is GET”，以及“Use CTFHub Method. I will give you flag.”，意思是要换掉默认的 GET 方法。说明考点就在请求行的方法上，必须改成题目要求的方法。我用 Burp 代理拦截这个请求，在 Repeater 里把请求行开头的 GET 直接改成 CTFHUB 再发送。响应返回 200，body 里出现 good job! 和 flag。

## 关键请求/响应

```http
CTFHUB /index.php HTTP/1.1
Host: challenge-416307d3f399d99.sandbox.ctfhub.com:10800

HTTP/1.1 200 OK
Allow: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH, CTFHUB
...
good job! ctfhub{8c13107b8cf1e51c40ba2109}
```

## 原理与复盘

请求行由「方法 + 请求目标 + HTTP 版本」三部分组成，方法在最前面。服务端会按方法走不同分支，如果只在方法名下做判断而不加限制，换一个方法就能进到原本不给普通 GET 的分支里。

---

## 截图

![请求方式](../imgs/lab5_http_method.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


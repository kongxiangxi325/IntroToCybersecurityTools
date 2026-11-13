# WP：请求方式

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 请求方式
> **任务**：按题目要求使用指定的 HTTP 方法访问目标，拿到 flag。
> **提示**：浏览器地址栏默认发送 GET 请求。用 Burp Repeater 修改请求行中的方法，或者用 `curl -X` 复现。
> **截图要求**：优先使用 Burp Repeater，截图中要能看到修改后的请求行（方法 + 路径）和响应中的 flag；如果 Burp 无法启动，可以用 `curl -X` 的方法修改截图代替，并在 WP 中说明原因。只有浏览器普通 GET 访问不算完成。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-9e6d5f04e6142319.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{d9e218bcbcb06ab8a7db27ae} |

## 解题过程

打开题目后，浏览器访问 `/index.php`，页面只显示与 HTTP 方法相关的提示，没有 flag，说明服务端是按请求方法区分处理的。我打开 Burp 并开启 Proxy → Intercept，刷新页面拦截到一条 `GET /index.php` 请求；在请求编辑区把请求行第一个词 `GET` 改成 `CTFHUB`，其余请求头原样保留，点 Forward 放行。浏览器页面随即返回 `good job! ctfhub{d9e218bcbcb06ab8a7db27ae}`。这说明服务端只对自定义的 `CTFHUB` 方法返回 flag，默认的 GET 会被拒绝。

## 关键请求/响应

```http
CTFHUB /index.php HTTP/1.1
Host: challenge-9e6d5f04e6142319.sandbox.ctfhub.com:10800
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Referer: http://challenge-9e6d5f04e6142319.sandbox.ctfhub.com:10800/index.php
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

good job! ctfhub{d9e218bcbcb06ab8a7db27ae}
```

## 原理与复盘

这道题对应 HTTP 报文的 **请求行**。请求行由“方法 + 请求目标 + HTTP 版本”组成，方法位于最前面、第一个空格之前。服务器通常根据方法决定如何处理请求；如果服务端没有严格限制可用方法，攻击者就可以用自定义方法绕过前端检查，拿到预期之外的内容。

---

## 截图

![请求方式](https://raw.githubusercontent.com/liukuoming/IntroToCybersecurityTools/lab5-submit/2026010030%E5%88%98%E9%98%94%E5%90%8D/Lab5/imgs/lab5_http_method.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

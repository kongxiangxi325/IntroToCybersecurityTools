# WP：302 跳转

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 302 跳转
> **任务**：观察 302 重定向，按题目提示找到 flag。
> **提示**：浏览器通常会自动跟随 302，所以你可能只看到最终页面。打开 DevTools 的 Network 面板（勾选 Preserve log）或 Burp，查看原始响应中的 `302` 状态码和 `Location` 响应头。
> **截图要求**：能看到 302 状态码和/或 `Location` 响应头，以及最终的 flag。只截最终页面、没有 302 证据的截图不合格。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-91921174854df8a1.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{468ff017654153f7eaef5f74} |

## 解题过程

打开题目后，浏览器访问 `/index.html`，页面只显示「No Flag here!」和一个「Give me Flag」链接，没有 flag。点击「Give me Flag」时页面会请求 `/index.php`，但浏览器立刻又跳回 `index.html`，看起来什么都没发生。为了看清跳转前的真实响应，我打开 Burp 的 Proxy → HTTP history，找到那条 `GET /index.php` 请求：状态码是 `302 Moved Temporarily`，响应头里有 `Location: /index.html`，而 302 的响应体里正是 flag。浏览器会自动跟随 Location，把这段 302 响应连同响应体隐藏掉了，所以只盯最终页面永远看不到 flag，必须看原始报文。

## 关键请求/响应

```http
GET /index.php HTTP/1.1
Host: challenge-91921174854df8a1.sandbox.ctfhub.com:10800

HTTP/1.1 302 Moved Temporarily
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 02:17:44 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/5.6.40
Location: /index.html
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 33

ctfhub{468ff017654153f7eaef5f74}
```

## 原理与复盘

这道题对应 HTTP 报文的 **状态行 + Location 响应头**。302 表示临时重定向，服务器通过 `Location` 告诉浏览器应该去的新地址；浏览器会自动跟随跳转。如果只盯着最终页面看，就会漏掉 302 这个关键信息，而攻击者（或安全测试人员）需要查看原始响应才能判断是否存在未授权跳转、开放重定向等风险。

---

## 截图

![302 跳转](https://raw.githubusercontent.com/liukuoming/IntroToCybersecurityTools/lab5-submit/2026010030%E5%88%98%E9%98%94%E5%90%8D/Lab5/imgs/lab5_redirect_302.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

# WP：302 跳转

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 302 跳转
> **任务**：观察 302 重定向，按题目提示找到 flag。
> **提示**：浏览器通常会自动跟随 302，所以你可能只看到最终页面。打开 DevTools 的 Network 面板（勾选 Preserve log）或 Burp，查看原始响应中的 `302` 状态码和 `Location` 响应头。
> **截图要求**：能看到 302 状态码和/或 `Location` 响应头，以及最终的 flag。只截最终页面、没有 302 证据的截图不合格。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 |http://challenge-2115f51620465970.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{4a7114d2e7922f0464063829} |

## 解题过程

看到点击获取flag，没有跳转，在proxy的HTTPhistory里找到302的记录，发送到repeat后在相应包里找到flag

## 关键请求/响应

```http
请求包
GET /index.php HTTP/1.1
Host: challenge-2115f51620465970.sandbox.ctfhub.com:10800
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-2115f51620465970.sandbox.ctfhub.com:10800/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
响应包
HTTP/1.1 302 Moved Temporarily
Server: openresty/1.21.4.2
Date: Fri, 23 Oct 2026 12:32:13 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/5.6.40
Location: /index.html
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 33
ctfhub{4a7114d2e7922f0464063829}
```

## 原理与复盘

200代表请求成功，浏览器直接渲染当前相应的页面。302是临时重定向，浏览器会发起新请求，跳转至location指定的网址

---

## 截图

![302 跳转](../imgs/lab5_redirect_302.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


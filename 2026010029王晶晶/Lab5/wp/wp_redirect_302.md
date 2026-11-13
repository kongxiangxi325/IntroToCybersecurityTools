# WP：302 跳转

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 302 跳转
> **任务**：观察 302 重定向，按题目提示找到 flag。
> **提示**：浏览器通常会自动跟随 302，所以你可能只看到最终页面。打开 DevTools 的 Network 面板（勾选 Preserve log）或 Burp，查看原始响应中的 `302` 状态码和 `Location` 响应头。
> **截图要求**：能看到 302 状态码和/或 `Location` 响应头，以及最终的 flag。只截最终页面、没有 302 证据的截图不合格。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-2115f5f2e0458970.sandbox.ctfhub.com:10800/index.php |
| Flag | ctfhub{4a7114d2e7922f0464063829} |

## 解题过程

直接用浏览器访问 /index.php，页面立刻跳到了 /index.html，什么都看不到。我推测 302 重定向会把关键内容藏在原始响应里，浏览器自动跟随后就看不到了。于是用 Burp 拦截这个请求，在响应里看到 302 Moved Temporarily 和 Location: /index.html，而响应体里已经带着 flag。

## 关键请求/响应

```http
GET /index.php HTTP/1.1
Host: challenge-2115f5f2e0458970.sandbox.ctfhub.com:10800

HTTP/1.1 302 Moved Temporarily
Location: /index.html
...
ctfhub{4a7114d2e7922f0464063829}
```

## 原理与复盘

关键在状态行和 Location 响应头。302 表示临时重定向，浏览器看到就会自动跳转，所以用户只看到最终页面；用 Burp 或 curl -i 看原始响应，才能发现被跳转掩盖的内容。

---

## 截图

![302 跳转](../imgs/lab5_redirect_302.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


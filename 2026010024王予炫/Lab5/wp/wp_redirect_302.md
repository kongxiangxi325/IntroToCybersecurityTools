# WP：302 跳转

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 302 跳转
> **任务**：观察 302 重定向，按题目提示找到 flag。
> **提示**：浏览器通常会自动跟随 302，所以你可能只看到最终页面。打开 DevTools 的 Network 面板（勾选 Preserve log）或 Burp，查看原始响应中的 `302` 状态码和 `Location` 响应头。
> **截图要求**：能看到 302 状态码和/或 `Location` 响应头，以及最终的 flag。只截最终页面、没有 302 证据的截图不合格。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-da9ad2f9e633a899.sandbox.ctfhub.com:10800（请求路径 `/index.php`） |
| Flag | ctfhub{eb8a039d211a7481d34bd6d9} |

## 解题过程

在 Firefox 里打开靶场地址，地址栏很快变成 `/index.html`，页面上只有一句“No Flag here!”，看不出任何可疑的东西 —— 说明浏览器已经自动把中间那次跳转走完了。为了看到被“跳过去”的那一跳，我改用 Kali 终端里的 `curl -i http://challenge-da9ad2f9e633a899.sandbox.ctfhub.com:10800/index.php`，并且故意**不加 `-L`**：curl 默认不跟随重定向，所以直接把原始响应打印出来。响应第一行就是 `HTTP/1.1 302 Moved Temporarily`，响应头里有 `Location: /index.html`，而真正有用的东西在响应体里 —— `ctfhub{eb8a039d211a7481d34bd6d9}`。我又加了一次 `-L` 做对照，跟随跳转后拿到的是 `/index.html`，响应体里只剩 `<title>No Flag here!</title>`，正好说明 flag 只在 302 那一跳里。提交 flag，通过。

## 关键请求/响应

```http
GET /index.php HTTP/1.1
Host: challenge-da9ad2f9e633a899.sandbox.ctfhub.com:10800
（curl 未加 -L，不跟随重定向）

HTTP/1.1 302 Moved Temporarily
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 13:30:12 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/5.6.40
Location: /index.html

ctfhub{eb8a039d211a7481d34bd6d9}

# 对照：加 -L 跟随跳转后，响应体里只剩
<title>No Flag here!</title>
```

## 原理与复盘

`302` 和 `200` 的区别在**状态行**和有没有 `Location`：`200` 是“这就是最终内容”，而 `302` 是“内容不在这，去 `Location` 指的地址拿”，本身几乎不带正文。浏览器会自动跟随 302，所以人眼只看到终点页；curl 不加 `-L`、或者 DevTools/Burp 里看原始响应，才能看到中间那一跳的完整报文。本题的坑就在这：真正的 flag 藏在被跳过的 302 响应体里，跟着跳就永远看不见。

---

## 截图

![302 跳转](../imgs/lab5_redirect_302.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

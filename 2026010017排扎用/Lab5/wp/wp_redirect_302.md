# WP：302 跳转

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 302 跳转
> **任务**：观察 302 重定向，按题目提示找到 flag。
> **提示**：浏览器通常会自动跟随 302，所以你可能只看到最终页面。打开 DevTools 的 Network 面板（勾选 Preserve log）或 Burp，查看原始响应中的 `302` 状态码和 `Location` 响应头。
> **截图要求**：能看到 302 状态码和/或 `Location` 响应头，以及最终的 flag。只截最终页面、没有 302 证据的截图不合格。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-7bedc1c63c617ccd.sandbox.ctfhub.com:10800/index.php |
| Flag | ctfhub{9f4e2bc6a7e045c6e9997865} |

## 解题过程

第一次在浏览器里访问靶场地址，页面看起来很正常，地址栏却已经不是 `index.php` 了，说明浏览器自动跟着跳转走了一次，我什么也没看到。我打开 DevTools 的 Network 面板并勾选 Preserve log 重新刷新，能看到 `index.php` 那条记录的状态码是 302，跳到另一个页面，但浏览器把中间那条响应体丢掉了。为了看清原始响应，我把 Burp 挂上、把请求 Send to Repeater 后直接 Send：Response 里显示 `HTTP/1.1 302 Moved Temporarily`，响应头有 `Location: /index.html` 和 `Content-Length: 33`，而响应体里正是那一行 flag。也就是说，服务端在重定向的那次响应里就把 flag 塞进了 body，只是浏览器自动跳转让人看不到。

## 关键请求/响应

```http
GET /index.php HTTP/1.1
Host: challenge-7bedc1c63c617ccd.sandbox.ctfhub.com:10800
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Referer: http://challenge-7bedc1c63c617ccd.sandbox.ctfhub.com:10800/
Connection: keep-alive

HTTP/1.1 302 Moved Temporarily
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 16:43:33 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/5.6.40
Location: /index.html
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 33

ctfhub{9f4e2bc6a7e045c6e9997865}
```

如果用 curl，加 `-i` 能看到状态行和 `Location`，但要注意 **不要加 `-L`**，否则 curl 也会和浏览器一样自动跳走，就看不到这条 302 的响应体了。

## 原理与复盘

302 属于状态行里的**状态码**，`Location` 属于**响应头**，两者配合完成一次临时重定向：浏览器收到后会自动再发一次请求到 `Location` 指的地址，所以用户只看到最终页面，中间那次响应被隐藏了。这和 200 的区别在于，200 是“内容就在这里，直接渲染响应体”，而 302 是“内容不在这里，去别处拿”，响应体经常被当成可忽略的附注——这题恰好把 flag 放在了这个被忽略的位置。安全上要注意：302 的目标地址如果来自用户输入，就可能被用作开放重定向钓鱼，服务端应该把 `Location` 限制在白名单内。

---

## 截图

![302 跳转](../imgs/lab5_redirect_302.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

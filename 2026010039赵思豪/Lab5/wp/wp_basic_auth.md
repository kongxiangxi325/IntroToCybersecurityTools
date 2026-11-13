# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-ff5a732ff14da347.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{29de284788437c6e03fe010c} |

## 解题过程

我在 Kali 里访问靶场的 /flag.html，浏览器直接弹出登录框，用 curl 一看，原始响应是 `401 Unauthorized`，并且带着 `WWW-Authenticate: Basic realm="..."`——这是 HTTP Basic 认证在要求凭据。题目页面还贴心地提示了默认用户名是 admin，并给了一个 10M 的密码字典，于是我直接用 hydra 对该页面做 HTTP GET 认证爆破（字典用 rockyou.txt 前段），很快跑出密码 `letmein`。最后用 `curl -u admin:letmein` 重新请求，curl 会把 `admin:letmein` 编码成 Base64 放进 `Authorization: Basic YWRtaW46bGV0bWVpbg==` 请求头，服务器认证通过，返回 200 和 flag。

## 关键请求/响应

```http
爆破结果：

[10000][http-get] host: challenge-ff5a732ff14da347.sandbox.ctfhub.com
                  login: admin   password: letmein

认证成功的关键请求（等价于 curl -u admin:letmein）：

GET /flag.html HTTP/1.1
Host: challenge-ff5a732ff14da347.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46bGV0bWVpbg==

响应 200，响应体：

ctfhub{29de284788437c6e03fe010c}
```

## 原理与复盘

Base64 不是加密，只是一种编码，拿到 `YWRtaW46bGV0bWVpbg==` 任何人都能秒解出 `admin:letmein`，所以 Basic 认证必须在 HTTPS 上使用，否则等于明文传密码。Authorization 请求头里实际放的就是“用户名:密码”的 Base64 编码，而 `WWW-Authenticate` 响应头则是服务器在 401 响应里告诉客户端“请用 Basic 方式重新带上凭据”。这道题还说明弱口令 + 可爆破的 Basic 认证非常脆弱，服务端应该限制尝试次数并强制强密码。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


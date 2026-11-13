# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-c4e36e253153c7af.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{3b53e3d4c4ec0322170a916b} |

## 解题过程

打开靶场，首页写着 "Here is your flag: click"，点击后访问 `/flag.html`，服务器返回 `401 Unauthorized`，响应头里还有 `WWW-Authenticate: Basic realm="Do u know admin ?"`——realm 提示用户名大概率是 admin。我先手工试了 admin/123456 等常见密码都是 401，确认这是要爆破的题。题目附件给了一个常见密码字典（top100），我在 Kali 终端里写了个 Python 脚本：逐个把 `admin:密码` 做 Base64 编码放进 `Authorization` 头发请求，看哪个返回 200。跑到第 52 个词 `baseball` 时返回 200，响应体里就是 flag。`admin:baseball` 的 Base64 编码是 `YWRtaW46YmFzZWJhbGw=`，解码后就是明文用户名密码，也验证了 Base64 只是编码不是加密。提交 flag 正确。

## 关键请求/响应

```http
GET /flag.html HTTP/1.1
Host: challenge-c4e36e253153c7af.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46YmFzZWJhbGw=
User-Agent: Python-http.client

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

ctfhub{3b53e3d4c4ec0322170a916b}
```

未认证时的响应：

```http
GET /flag.html HTTP/1.1

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Do u know admin ?"
```

## 原理与复盘

Base64 不是加密，只是一种编码，任何人拿到 `Authorization` 头里的字符串都能瞬间解码出 `用户名:密码` 明文，所以 Basic 认证必须配合 HTTPS 使用，否则凭据等于明文广播。Authorization 请求头里放的实际就是 `用户名:密码` 的 Base64 编码。这个题还说明弱口令 + 无登录次数限制的认证基本形同虚设，用常见密码字典几秒钟就能跑穿；防御上应限制失败尝试次数并使用强密码。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

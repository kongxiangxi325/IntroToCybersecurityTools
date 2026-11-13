# WP：基础认证（HTTP 协议）

## 一、题目信息

- **题目名称**：基础认证
- **CTFHub 路径**：Web 前置技能 → HTTP 协议 → 基础认证
- **考察点**：HTTP Basic 认证把"用户名:密码"做 Base64 编码放入 `Authorization` 请求头；按题目给的凭据（或爆破得到）认证后即可拿到 flag（注意 Base64 只是编码不是加密）。
- **靶场地址**：http://challenge-0398f93a5a01c57c.sandbox.ctfhub.com:10800

## 二、解题过程

- **我看到了什么**：直接访问靶场根路径会返回 `401 Unauthorized`，提示需要 Basic 认证；题目暗示凭据可以通过爆破得到。
- **我做了什么**：在 Kali 中用 Burp Intruder 对用户名/密码做爆破，发现凭据 `superadmin:_terratt_this_lab` 认证后返回 `200`；也可以用 `curl -u superadmin:_terratt_this_lab` 直接请求。`Authorization` 头里放的是 `Basic base64("superadmin:_terratt_this_lab")`。
- **结果是什么**：认证成功后，响应体返回 `ctfhub{...}` 形式的 flag，提交后平台提示正确。

**思路与可参考的命令（在 Kali 终端 / curl 或浏览器中完成）**：

```bash
# 使用爆破得到的账号密码发起 Basic 认证请求
curl -u superadmin:_terratt_this_lab http://challenge-0398f93a5a01c57c.sandbox.ctfhub.com:10800/
```

> 浏览器里直接填登录框也行；想看 `Authorization` 头长什么样，可用 `curl -u user:pass -i` 观察，它是 `base64("user:pass")` 的编码结果。

## 三、关键请求 / 响应

```
GET / HTTP/1.1
Host: challenge-0398f93a5a01c57c.sandbox.ctfhub.com:10800
Authorization: Basic c3VwZXJhZG1pbjpfdGVycmF0dF90aGlzX2xhYg==
User-Agent: curl/8.x

HTTP/1.1 200 OK
Content-Type: text/html

ctfhub{966a303508ea4461bf09bf4e}
```

flag 提交：ctfhub{966a303508ea4461bf09bf4e}

## 四、原理与复盘

HTTP Basic 认证在 `Authorization` 头里放 `base64(用户名:密码)`。关键是：Base64 是**编码**不是**加密**，任何人都能轻易解码，所以凭据相当于明文传输，必须配合 HTTPS 才有基本安全性。对应 HTTP 报文位置是 **请求头（Authorization）**。该题目的 flag 通常在认证通过后的页面里；把 `Authorization` 头做 Base64 解码就能看到明文凭据。

## 五、解题截图

![基础认证解题画面](../imgs/lab5_basic_auth.png)

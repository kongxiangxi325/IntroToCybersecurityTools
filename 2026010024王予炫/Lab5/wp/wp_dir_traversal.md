# WP：目录遍历

> **CTFHub 路径**：技能树 → Web → 信息泄露 → 目录遍历
> **任务**：按题目页面提示找到 flag。
> **提示**：注意页面给出的路径和 URL；目录列表本身就是一种信息泄露。只在题目环境内点击和访问，不要使用扫描器扫描其他地址。
> **截图要求**：能看到题目环境地址（或题目名称）、你访问的目录/路径，以及最终的 flag。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-ec5691edac044bbb.sandbox.ctfhub.com:10800 |
| Flag | ctfhub{d4a29b15d00848b082a41654} |

## 解题过程

开启题目后我访问靶场首页，页面提示与“目录”有关，于是我直接在地址后面加上 `/flag_in_here/` 访问。服务器返回的不是报错页，而是 Apache 自动生成的目录列表，页面上只有 `Parent Directory` 和 `1/`、`2/`、`3/`、`4/` 四个子目录，没有任何正文——这说明该目录没有索引页，同时目录浏览（Indexes）是开着的。我按列表逐个点进去，在 `3/` 下面还有一个 `1/`，进去后就看到了 `flag.txt`。访问 `/flag_in_here/3/1/flag.txt`，返回 `200 OK`、`Content-Type: text/plain`、`Content-Length: 33`，响应体的纯文本就是 flag。回到题目页面提交，平台提示正确。

## 关键请求/响应

```http
GET /flag_in_here/ HTTP/1.1
Host: challenge-ec5691edac044bbb.sandbox.ctfhub.com:10800

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Content-Type: text/html; charset=UTF-8

<title>Index of /flag_in_here</title>
Parent Directory    1/    2/    3/    4/

GET /flag_in_here/3/1/flag.txt HTTP/1.1
Host: challenge-ec5691edac044bbb.sandbox.ctfhub.com:10800

HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Sat, 24 Oct 2026 13:37:11 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 33
Last-Modified: Sat, 24 Oct 2026 13:35:30 GMT
ETag: "21-65e962ba3aeb5"
Accept-Ranges: bytes

ctfhub{d4a29b15d00848b082a41654}
```

## 原理与复盘

这道题动的是请求行里的**请求 URI**：把路径换成 `/flag_in_here/3/1/flag.txt`，服务器就按这个路径去磁盘上取文件，flag 最后出现在**响应体**里（`text/plain`）。目录列表之所以算信息泄露，是因为服务器把“这个目录里有什么”直接渲染成 HTML 返回，攻击者不用猜文件名就能看到备份文件、源码、配置和本该隐藏的 flag.txt。防护上应该在 Web 服务器配置里关掉目录浏览，并给每个目录补上默认索引页。

---

## 截图

![目录遍历](../imgs/lab5_dir_traversal.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

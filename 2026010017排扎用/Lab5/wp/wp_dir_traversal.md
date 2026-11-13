# WP：目录遍历

> **CTFHub 路径**：技能树 → Web → 信息泄露 → 目录遍历
> **任务**：按题目页面提示找到 flag。
> **提示**：注意页面给出的路径和 URL；目录列表本身就是一种信息泄露。只在题目环境内点击和访问，不要使用扫描器扫描其他地址。
> **截图要求**：能看到题目环境地址（或题目名称）、你访问的目录/路径，以及最终的 flag。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-45186a87ea6ec8c7.sandbox.ctfhub.com:10800/flag_in_here/3/2/flag.txt |
| Flag | ctfhub{126477d5222b00ff6e995b6e} |

## 解题过程

开启题目后打开靶场地址，页面不是正常的网页，而是服务器直接列出来的目录列表，能看到 `flag_in_here` 目录以及它下面的 `1`、`2`、`3`、`4` 几个子目录。我先点进 `1`、`2`，发现里面还是可以继续点的子目录，一层层点下去看到的都是目录，没有 flag。回到 `3` 目录后点进它的 `2` 号子目录，里面直接列出了 `flag.txt`，点开这个文件，页面内容就是一行 flag。整个过程只是改 URL 里 `/flag_in_here/` 后面那几段路径，没有任何登录或验证，说明服务器对路径完全没有做限制，只要知道（或者猜出）路径就能读到文件。把 flag 提交到 CTFHub，平台提示正确。

## 关键请求/响应

```http
GET /flag_in_here/3/2/flag.txt HTTP/1.1
Host: challenge-45186a87ea6ec8c7.sandbox.ctfhub.com:10800
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

HTTP/1.1 200 OK
Content-Type: text/plain

ctfhub{126477d5222b00ff6e995b6e}
```

本题不需要修改请求（不用改方法、不用加 Cookie），只是把请求行里的路径一段段往下点：先在首页看到 `flag_in_here/` 下的 `1`、`2`、`3`、`4` 几个目录链接，逐级点进 `3/`、`3/2/` 后，目录列表里出现 `flag.txt`，点开就是上面的响应。整个过程中服务器一直是把目录内容当普通页面返回，没有任何权限校验。

## 原理与复盘

这道题对应 HTTP 报文中最前面的**请求行里的 URL 路径**：服务器把路径直接映射到磁盘目录，`/flag_in_here/3/2/flag.txt` 就对应站点根目录下的同名文件。因为 Web 服务器开了目录列表（autoindex），访问一个目录时会把里面的文件名列出来，攻击者就能像浏览文件管理器一样一层层翻，找到备份文件、源码、配置甚至 flag。防御上应该关掉目录列表、把敏感文件放在 Web 根目录之外，并对路径做规范化校验，挡住 `../` 这类越权访问。

---

## 截图

![目录遍历](../imgs/lab5_dir_traversal.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

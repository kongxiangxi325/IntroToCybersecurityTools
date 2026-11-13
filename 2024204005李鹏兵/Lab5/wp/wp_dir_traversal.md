# WP：目录遍历

> **CTFHub 路径**：技能树 → Web → 信息泄露 → 目录遍历
> **任务**：按题目页面提示找到 flag。
> **提示**：注意页面给出的路径和 URL；目录列表本身就是一种信息泄露。只在题目环境内点击和访问，不要使用扫描器扫描其他地址。
> **截图要求**：能看到题目环境地址（或题目名称）、你访问的目录/路径，以及最终的 flag。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-7064c119bbb6f879.sandbox.ctfhub.com:10800/ |
| Flag | ctfhub{20160ad52ea9438449fac1a0} |

## 解题过程

打开题目地址后，页面上只有一个 flag_in_here 目录，点进去看到 1、2、3、4 四个文件夹，服务器把目录里的内容直接列了出来。我按顺序逐个点开，前几个目录里只有下一层子目录，没有 flag。点进 2 目录后里面又出现 1、2、3、4 四个子目录，继续往下进入 2/4，看到一个 flag.txt 文件。点开 flag.txt，页面里只有一行 ctfhub{20160ad52ea9438449fac1a0}，回到题目页面提交后提示正确。

## 关键请求/响应

```http
GET /flag_in_here/2/4/flag.txt HTTP/1.1
Host: challenge-7064c119bbb6f879.sandbox.ctfhub.com:10800
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Connection: keep-alive

HTTP/1.1 200 OK
（响应体只有一行）

ctfhub{20160ad52ea9438449fac1a0}
```

本题没有改包，全程是浏览器里点目录列表，上面的请求就是点开 flag.txt 时浏览器发出的那条。

## 原理与复盘

这对应 HTTP 响应报文的响应体：服务器开启了目录索引，当目录下没有 index.html 这类默认首页时，就把目录里的文件名以 HTML 列表的形式打印出来。列表里可能有备份文件、源码、配置文件，攻击者顺着目录一层层点下去就能拿到本来无权访问的东西，属于典型的信息泄露。修复方式是在 Web 服务器里关掉目录索引（Apache 的 `Options -Indexes`），并给敏感目录加访问控制。

---

## 截图

![目录遍历](../imgs/lab5_dir_traversal.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


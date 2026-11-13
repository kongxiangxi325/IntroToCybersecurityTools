# WP：PHPINFO

> **CTFHub 路径**：技能树 → Web → 信息泄露 → PHPINFO
> **任务**：在 phpinfo 页面中找到 flag，并观察它泄露了哪些信息。
> **提示**：phpinfo 会输出大量 PHP 和服务器配置。用浏览器的查找功能搜索关键字，同时留意页面暴露的路径、版本、环境变量等信息。
> **截图要求**：能看到 phpinfo 页面、你搜索/定位到的 flag，以及至少一处敏感信息。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-3b5c4ce175453a7e.sandbox.ctfhub.com:10800/phpinfo.php |
| Flag | ctfhub{193d5db7d5ddc394bd67ea30} |

## 解题过程

题目提示站点有信息泄露点，需要自己找到暴露的页面。我先看首页没什么线索，就试着访问常见的 phpinfo.php，页面果然返回了完整的 PHP 环境信息。接着用浏览器查找关键字 ctfhub，一共命中 7 处，其中环境变量里的 FLAG 那一行就是答案。页面上还能看到 Apache 运行用户、文档根目录、请求头等大量环境信息。

## 关键请求/响应

```http
GET /phpinfo.php HTTP/1.1
Host: challenge-3b5c4ce175453a7e.sandbox.ctfhub.com:10800

本题不需要修改请求。响应体 Environment 区域的 FLAG 变量为：
FLAG  ctfhub{193d5db7d5ddc394bd67ea30}
```

## 原理与复盘

这道题对应响应体。phpinfo 会输出环境变量、路径、模块和配置信息，一旦留在生产环境，等于把服务器内部情况直接交给攻击者，是渗透测试里很常见的入口线索。

---

## 截图

![PHPINFO](../imgs/lab5_phpinfo.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


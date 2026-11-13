# WP：PHPINFO

> **CTFHub 路径**：技能树 → Web → 信息泄露 → PHPINFO
> **任务**：在 phpinfo 页面中找到 flag，并观察它泄露了哪些信息。
> **提示**：phpinfo 会输出大量 PHP 和服务器配置。用浏览器的查找功能搜索关键字，同时留意页面暴露的路径、版本、环境变量等信息。
> **截图要求**：能看到 phpinfo 页面、你搜索/定位到的 flag，以及至少一处敏感信息。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-385bc4ce175453a7e.sandbox.ctfhub.com:10800/phpinfo.php |
| Flag | ctfhub{b1354ceb7d5d41c94b7eea301} |

## 解题过程

打开题目地址后直接就是 phpinfo 页面，不需要点任何按钮。按住 Ctrl + F 输入 ctfhub 回车，浏览器会跳到高亮的那一处，正好是 Environment 一节里的 FLAG 变量，值就是 flag。除了 flag，页面还暴露了 Apache 的运行目录、日志目录、运行用户 www-data，以及 PHP 版本 7.3.14 和访问者 IP 等信息。

## 关键请求/响应

```http
GET /phpinfo.php HTTP/1.1
Host: challenge-385bc4ce175453a7e.sandbox.ctfhub.com:10800

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

（响应体 Environment 一节中定位到的字段）
Variable              Value
APACHE_RUN_DIR        /var/run/apache2
APACHE_LOG_DIR        /var/log/apache2
APACHE_RUN_USER       www-data
FLAG                  ctfhub{b1354ceb7d5d41c94b7eea301}

（响应体 PHP Variables 一节）
$_SERVER['HTTP_HOST']    challenge-385bc4ce175453a7e.sandbox.ctfhub.com:10800
```

## 原理与复盘

phpinfo 页面一般会暴露 PHP 版本、服务器操作系统、网站物理路径、环境变量、扩展信息等。攻击者利用这些信息收集服务器指纹，再查找相应漏洞进行攻击；本次的 flag 就直接写在环境变量里，被 phpinfo 原样打印了出来。

---

## 截图

![PHPINFO](../imgs/lab5_phpinfo.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

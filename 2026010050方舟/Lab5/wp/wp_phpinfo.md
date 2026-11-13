# WP：PHPINFO

> **CTFHub 路径**：技能树 → Web → 信息泄露 → PHPINFO
> **任务**：在 phpinfo 页面中找到 flag，并观察它泄露了哪些信息。
> **提示**：phpinfo 会输出大量 PHP 和服务器配置。用浏览器的查找功能搜索关键字，同时留意页面暴露的路径、版本、环境变量等信息。
> **截图要求**：能看到 phpinfo 页面、你搜索/定位到的 flag，以及至少一处敏感信息。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-cfac12d5b81ae191.sandbox.ctfhub.com:10800/phpinfo.php |
| Flag | ctfhub{44bb539d931960eb397748eb} |

## 解题过程

打开靶场给的地址，只有一个 `phpinfo.php` 页面，满屏都是 PHP 配置项，正常往下翻根本翻不到底。我先用浏览器的页面查找（`Ctrl + F`）搜 `ctfhub{`，页面直接跳到 `Environment` 环境变量表里，`FLAG` 这个变量的值就是 `ctfhub{44bb539d931960eb397748eb}`，把它复制回平台提交就通过了。找 flag 的同时我顺手看了同一页还暴露了什么：`APACHE_RUN_USER`、`APACHE_LOG_DIR`、`PWD` 这些环境变量说明了 web 目录和运行用户，`PHP Variables` 里的 `_SERVER["SERVER_SOFTWARE"]` 写出了 Apache 2.4.38 (Debian)，`_SERVER["SERVER_ADDR"]` 是容器内网 IP，`DOCUMENT_ROOT` 直接把网站绝对路径给了出来。这些都是后面做渗透时用来挑版本漏洞、找上传目录的情报，所以 phpinfo 页面在生产环境里是绝对不能留的。

## 关键请求/响应

```http
GET /phpinfo.php HTTP/1.1
Host: challenge-cfac12d5b81ae191.sandbox.ctfhub.com:10800
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

（响应体是一大段 phpinfo 表格，关键的两处摘录如下）
Environment 表：
  PWD          /
  FLAG         ctfhub{44bb539d931960eb397748eb}
PHP Variables 表：
  _SERVER["SERVER_SOFTWARE"]  Apache/2.4.38 (Debian)
  _SERVER["DOCUMENT_ROOT"]    /var/www/html
```

## 原理与复盘

phpinfo 是 PHP 自带的调试页面，位置在**响应体**：它会一次性输出 PHP 版本、编译参数、模块、`Environment` 和 `PHP Variables` 里的环境变量、绝对路径、内网 IP 等。对攻击者来说这是一份免费的情报清单——知道版本就能查对应 CVE，知道绝对路径就能配合文件包含或上传定位木马，知道内网地址就能规划横向。这道题的 flag 干脆就放在 `FLAG` 环境变量里，等于把“phpinfo 会泄露环境变量”这件事直接演了一遍；实务中的结论很简单：线上环境不要留 `phpinfo.php`，调试完就删。

---

## 截图

![PHPINFO](../imgs/lab5_phpinfo.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

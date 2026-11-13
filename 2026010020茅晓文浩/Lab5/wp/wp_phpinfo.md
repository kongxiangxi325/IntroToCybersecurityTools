# WP：PHPINFO

> **CTFHub 路径**：技能树 → Web → 信息泄露 → PHPINFO
> **任务**：在 phpinfo 页面中找到 flag，并观察它泄露了哪些信息。
> **提示**：phpinfo 会输出大量 PHP 和服务器配置。用浏览器的查找功能搜索关键字，同时留意页面暴露的路径、版本、环境变量等信息。
> **截图要求**：能看到 phpinfo 页面、你搜索/定位到的 flag，以及至少一处敏感信息。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-fe11aeeda6d042f4.sandbox.ctfhub.com:10800/phpinfo.php |
| Flag | ctfhub{f02bf340d382b3f65af2a9ce} |

## 解题过程

开启题目后访问靶场，页面直接就是一份完整的 `phpinfo()` 输出，标签页标题是 `PHP 7.3.14 - phpinfo()`。页面很长，我先扫了顶部的版本信息，看到 PHP 7.3.14、`Apache/2.4.38 (Debian)`、`DOCUMENT_ROOT` 是 `/var/www/html`，这些本来都不该公开。然后用 `Ctrl + F` 搜索 `flag`，页面跳到 **Environment** 表格，其中一行 `FLAG` 的值就是 flag。复制回题目页面提交，平台提示正确。

## 关键请求/响应

```http
GET /phpinfo.php HTTP/1.1
Host: challenge-fe11aeeda6d042f4.sandbox.ctfhub.com:10800

HTTP/1.1 200 OK
Server: Apache/2.4.38 (Debian)
X-Powered-By: PHP/7.3.14
Content-Type: text/html; charset=UTF-8

...
<tr><td class="e">FLAG</td><td class="v">ctfhub{f02bf340d382b3f65af2a9ce}</td></tr>
<tr><td class="e">DOCUMENT_ROOT</td><td class="v">/var/www/html</td></tr>
...
```

本题不需要修改请求，flag 就写在 `phpinfo.php` 的响应体里。

## 原理与复盘

`phpinfo()` 是调试函数，会把 PHP 版本、编译参数、扩展模块、`DOCUMENT_ROOT`、环境变量甚至数据库配置全部打印到**响应体**里，本题的 flag 就被放在环境变量 `FLAG` 中，随 **Environment** 表格一起输出。这些信息对攻击者很有用：版本号可以对应已知漏洞，绝对路径可以配合文件包含或目录遍历，环境变量里可能直接有密码和密钥。所以生产环境必须删掉 `phpinfo.php` 这类调试页面。

---

## 截图

![PHPINFO](../imgs/lab5_phpinfo.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

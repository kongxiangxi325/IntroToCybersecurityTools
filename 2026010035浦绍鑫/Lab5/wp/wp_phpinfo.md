# WP：PHPINFO

> **CTFHub 路径**：技能树 → Web → 信息泄露 → PHPINFO
> **任务**：在 phpinfo 页面中找到 flag，并观察它泄露了哪些信息。
> **提示**：phpinfo 会输出大量 PHP 和服务器配置。用浏览器的查找功能搜索关键字，同时留意页面暴露的路径、版本、环境变量等信息。
> **截图要求**：能看到 phpinfo 页面、你搜索/定位到的 flag，以及至少一处敏感信息。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-35b5c4ce175453a7e.sandbox.ctfhub.com:10800/phpinfo.php |
| Flag | ctfhub{1959d0b7653dc354bd67be30} |

## 解题过程

开启靶场后直接访问环境地址，页面就是一个完整的 phpinfo() 输出页面。我先用浏览器的查找功能（Ctrl+F）搜索 FLAG 关键字，在页面上方的 Environment（环境变量）表格里找到了名为 FLAG 的变量，它的值就是 flag，我用鼠标选中提交通过了。除此之外我还注意到页面暴露了很多敏感信息：PHP 版本是 7.3.14，服务器是 Apache 2.4.38 (Debian)，还能看到 $_SERVER 里的各种路径、X-Real-IP 等真实 IP 信息。这道题说明 phpinfo 页面如果部署在生产环境，等于把服务器的配置全部公开了。

## 关键请求/响应

```http
GET /phpinfo.php HTTP/1.1
Host: challenge-35b5c4ce175453a7e.sandbox.ctfhub.com:10800

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

Environment 表格中：
FLAG    ctfhub{1959d0b7653dc354bd67be30}
```

## 原理与复盘

phpinfo 页面会输出 PHP 版本、扩展、环境变量、$_SERVER 等大量服务器内部信息。这些信息对攻击者非常有用：版本号可以用来匹配已知漏洞，路径可以辅助目录穿越，环境变量里甚至可能直接放着密码或 flag 这类敏感数据。所以上线环境必须删除 phpinfo 测试页面。

---

## 截图

![PHPINFO](../imgs/lab5_phpinfo.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。


# WP：PHPINFO

> **CTFHub 路径**：技能树 → Web → 信息泄露 → PHPINFO
> **任务**：在 phpinfo 页面中找到 flag，并观察它泄露了哪些信息。
> **提示**：phpinfo 会输出大量 PHP 和服务器配置。用浏览器的查找功能搜索关键字，同时留意页面暴露的路径、版本、环境变量等信息。
> **截图要求**：能看到 phpinfo 页面、你搜索/定位到的 flag，以及至少一处敏感信息。

---

## 题目信息

| 项目 | 内容 |
| --- | --- |
| 环境地址 | http://challenge-cb0e6ceeec96a6f8.sandbox.ctfhub.com:10800 |
| 题目入口 | `/`（按钮“点击查看phpinfo”）→ `/phpinfo.php` |
| Flag | ctfhub{fc9962f2e194595831e8bcc2} |

## 解题过程

打开靶场首页，页面只有一个标题 `phpinfo` 和一个绿色按钮“点击查看phpinfo”，链接指向 `phpinfo.php`。点进去以后页面变成一大片紫色表格，标题是 `PHP Version 7.3.14`，整页大概 80 KB。

这一页的表格从头翻到尾基本找不到东西，所以我没有肉眼扫，直接在 Kali 终端里把响应拉下来再筛：

```bash
U="http://challenge-cb0e6ceeec96a6f8.sandbox.ctfhub.com:10800"
curl -s "$U/phpinfo.php" -o /tmp/p.html
wc -c /tmp/p.html            # 81927，确实是一整页 phpinfo
grep -oiE "ctfhub\{[^}]*\}" /tmp/p.html
```

`grep` 只命中一次，位置在 **`Environment`（环境变量）** 这一节：变量名是 `FLAG`，值就是 flag。再往下翻到 `PHP Variables` 那一段，同样的值又以 `$_ENV['FLAG']` 的形式出现了一次——说明服务端是把 flag 作为环境变量注入容器的，phpinfo 把整个环境变量表原样打印了出来。

确认位置后，我又回到浏览器里用 `Ctrl + F` 搜 flag 的取值 `fc9962f2`，页面会自动滚到 `Environment` 那一段并把命中的值高亮出来（截图就是这一屏）。这一步是为了拿到“人工在页面上定位到 flag”的证据，和终端里 `grep` 的结果互相印证。

顺便在同一页记下了几处同样不该对外暴露的信息作为佐证：

- `System`：`Linux challenge-cb0e6ceeec96a6f8-5cc76f76dc-9kwkp 6.12.48+deb13-amd64 ... x86_64`，直接暴露了容器主机名和内核版本；
- `Server API`：`Apache 2.0 Handler`，结合响应头 `Server: Apache/2.4.38 (Debian)` 能确定整套运行栈；
- `Configuration File (php.ini) Path`：`/usr/local/etc/php`，泄露了服务端绝对路径；
- 同页 `Environment` 段里还有 `APACHE_RUN_USER`、`APACHE_LOG_DIR`、`PWD` 等容器运行时变量，把目录结构和运行账号也一起给出了。

把 flag 提交后提示正确。

## 关键请求/响应

```http
GET /phpinfo.php HTTP/1.1
Host: challenge-cb0e6ceeec96a6f8.sandbox.ctfhub.com:10800
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

HTTP/1.1 200 OK
Server: Apache/2.4.38 (Debian)
Content-Type: text/html; charset=UTF-8
Content-Length: 81928

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ...>
<html><head><title>PHP 7.3.14 - phpinfo()</title> ...
```

响应体里和本题有关的两处（原文，行号为响应体中的位置）：

```html
<!-- 第 746 行：Environment 段 -->
<h2><a name="module_environment" id="module_environment">Environment</a></h2>
<table>
<tr><td class="e">PWD </td><td class="v">/ </td></tr>
<tr><td class="e">FLAG </td><td class="v">ctfhub{fc9962f2e194595831e8bcc2} </td></tr>
</table>

<!-- 第 806 行：PHP Variables 段 -->
<tr><td class="e">$_ENV['PWD']</td><td class="v">/</td></tr>
<tr><td class="e">$_ENV['FLAG']</td><td class="v">ctfhub{fc9962f2e194595831e8bcc2}</td></tr>
```

同一页里的敏感信息（节选）：

```html
<tr><td class="e">System </td><td class="v">Linux challenge-cb0e6ceeec96a6f8-5cc76f76dc-9kwkp 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64 </td></tr>
<tr><td class="e">Server API </td><td class="v">Apache 2.0 Handler </td></tr>
<tr><td class="e">Configuration File (php.ini) Path </td><td class="v">/usr/local/etc/php </td></tr>
```

> 说明：上面只截取了 phpinfo 响应里和本题相关的几行，实际响应体有 80 KB 左右。整页里 `ctfhub` 这个关键字只在 `Environment` 和 `PHP Variables` 两处出现，指向的都是同一个环境变量 `FLAG`。

## 原理与复盘

这道题同样落在**响应体**，但泄露的层次比“目录遍历”更深一层：phpinfo 会把 PHP 版本、编译参数、`php.ini` 路径、`disable_functions`、扩展列表，以及 `_SERVER` / `_ENV` 里的**全部环境变量**一次性打印出来，本题的 flag 就是以环境变量的形式被打印出来的。

环境变量之所以危险，是因为现代部署（Docker、Kubernetes、CI）习惯把密码、API Key、数据库连接串放进环境变量。一旦 phpinfo 对外可达，等于把整份“配置清单”连同密钥一起送给访问者——本题的 flag 正是在模拟这种泄露。

这些信息对攻击者的价值在于“减少猜测”：知道精确的 PHP 版本（7.3.14）就能去查对应 CVE；知道绝对路径（`/usr/local/etc/php`）就能在文件包含、日志投毒里直接拼路径；知道 `disable_functions` 就能挑一个没被禁用的函数做命令执行；知道主机名和内网信息可以做横向定位。

根因是调试文件 `phpinfo.php` 上线后没删。防守上，生产环境必须删掉这类探针文件，或者至少用 `Require local` / 白名单限制只允许本机访问；同时敏感配置应放进密钥管理服务，而不是裸的环境变量。

---

## 截图

![PHPINFO](../imgs/lab5_phpinfo.png)

> 可以在这份 WP 中另加过程截图；检查时只看指定图片，额外图片不检查。

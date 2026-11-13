# Lab3：VMware 与 Kali 虚拟机环境搭建与验收

> **作业目标**：用命令输出和截图证明 Kali 虚拟机已正确配置并能联网，并能分别用 MobaXterm 和 VSCode Remote-SSH 从 Windows 宿主机远程连接这台虚拟机。
>
> **前置条件**：软件源用官方源即可，不需要更换。
>
> **命令执行方式**：下面所有命令请**一条一条执行**，每执行一条就先看清它的输出再执行下一条。不要把一节里的命令一次性全部粘贴进终端，否则输出会混在一起，看不出是哪条命令出了问题。
>
> **复制粘贴提示**：完成第七节（检查 VMware Tools）之前，命令需要手动敲进虚拟机终端；完成那一节之后，就可以把本文档里的命令直接复制粘贴进虚拟机了。
>
> **验收方式**：按第一至十五节的顺序搭建和检查，相关章节末尾有验收表格，并按文末「截图要求」截图；全部完成后填写「环境验收总结」，按「提交要求」提交。

---

## 一、实验背景

本课程是网络安全工具入门，实验需要一台 Linux 系统，并用到 Kali 预装的安全和网络工具（扫描、抓包、流量分析等）。直接在自己的 Windows 主机上做这些操作不现实，也不安全：

- Windows 和 Linux 的命令体系不同，课程用到的 `nmap`、`tcpdump`、`ssh`、`ip` 等命令都以 Linux 为准；
- 安全实验会反复扫描端口、抓取流量、修改系统配置，误操作可能影响自己的日常电脑；
- 万一环境被改坏，Linux 虚拟机可以直接删除重装，Windows 主机不能。

虚拟机的作用就是在一台真实电脑里再运行一台“虚拟电脑”。你可以把 Kali 安装在虚拟机中，像使用一台独立 Linux 主机一样操作它；即使工具误删、配置写错、系统改坏，也不会破坏宿主机。

本实验最终要得到一台能够正常启动、联网、打开终端、SSH 可远程登录的 Kali 虚拟机。第一次实验先把环境搭好，后面的实验都在这台虚拟机上完成。

---

## 二、准备文件

### 课程仓库中的文件

本目录（`homework/Lab3/`）只包含一个文档，安装手册与验收作业合并在一起：

```text
homework/Lab3/
└── Lab3.md
```

| 文件 | 作用 | 说明 |
| :--- | :--- | :--- |
| `Lab3.md` | 本文档：按顺序完成环境搭建与验收 | 按顺序完成即可 |

### 教师通过企业微信发送的文件

VMware 安装包和 Kali 镜像体积很大，不放在课程仓库中，由教师通过**企业微信**发送。请自行接收并保存到宿主机上一个方便查找的目录，例如 `D:\OSLab\`：

| 文件 | 作用 |
| :--- | :--- |
| `VMware-Workstation-Full-26H1-25388281.exe` | VMware Workstation Pro Windows 安装包，用于在 Windows 上安装虚拟机软件 |
| `kali-linux-2026.2-vmware-amd64.7z` | Kali Linux 2026.2 **预装 VMware 虚拟机**（Xfce 桌面，已装好系统，解压后直接使用，无需安装） |

> **注意**：这两个文件不要放进课程仓库的文件夹，也不要提交到 Git。仓库只用于提交作业文档、代码和截图，提交大文件会导致 PR 无法正常检查。

### 版本选择说明

- VMware 选择 **VMware Workstation Pro 26H1 for Windows**。
- Kali 选择 **Kali Linux 2026.2 预装 VMware 虚拟机**（文件名形如 `kali-linux-2026.2-vmware-amd64.7z`）。

选择预装虚拟机的原因：系统、桌面和常用安全工具都已经装好，解压打开就能用，省去安装系统的时间，也避免在安装器里误操作。Kali 是滚动更新的发行版，没有 LTS 的概念；本实验验收只要求 `VERSION` 不低于 2026.2。

### 官方下载地址

如果企业微信中的文件已过期或接收失败，可从以下官方入口下载：

- VMware Workstation Pro：<https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Workstation+Pro>
- Kali Linux 预装虚拟机：<https://cdimage.kali.org/kali-2026.2/>（选择 `kali-linux-2026.2-vmware-amd64.7z`；全部镜像见 <https://www.kali.org/get-kali/>）

> **注意**：VMware 当前由 Broadcom 分发，官方门户可能要求注册或登录。优先使用教师通过企业微信发送的安装包，可以省去注册和排队下载的时间。

---

## 三、宿主机要求与虚拟机配置

开始前先确认自己的电脑满足以下要求：

| 项目 | 最低要求 | 建议配置 |
| :--- | :--- | :--- |
| 操作系统 | Windows 10/11 64 位 | Windows 11 64 位 |
| 内存 | 8GB | 16GB 或以上 |
| 磁盘剩余空间 | 40GB | 80GB 或以上 |
| CPU | 支持虚拟化 | Intel VT-x 或 AMD-V 已开启 |
| 网络 | 可访问互联网 | 安装和更新软件包会用到 |

### 根据宿主机选择虚拟机配置

先在 Windows 的“任务管理器 → 性能”中查看宿主机的 CPU 核心数和内存，再在“此电脑”中查看存放虚拟机的磁盘剩余空间。按下表选择与自己宿主机匹配的档位：

| 宿主机情况 | 虚拟 CPU 总核心数 | 虚拟内存 | 虚磁盘上限 | 适用说明 |
| :--- | :---: | :---: | :---: | :--- |
| 8GB 内存，4 核左右，剩余 50GB 以上 | 2 核 | 4096MB | 40GB | 最低可用档；做实验时关闭宿主机上不必要的程序 |
| 16GB 内存，6 核以上，剩余 80GB 以上 | 2 核 | 6144MB | 60GB | **课程推荐档**；运行安全工具比较流畅 |
| 32GB 及以上内存，8 核以上，剩余 120GB 以上 | 4 核 | 8192MB | 80GB | 宽裕档；适合长期保留多个快照 |

> **选择规则**：宿主机同时满足该行的内存、CPU 和磁盘条件时，才选择该档。任意一项不满足时，选低一档。不要把宿主机的全部 CPU 或内存分给虚拟机，否则 Windows 和虚拟机都会变卡。

虚磁盘默认按实际使用量逐步增长，将上限设为 60GB 或 80GB 不代表创建时立即占用同等大小。但 VMware 快照会额外占用宿主机空间，学期内应定期检查剩余空间。

### 检查 CPU 虚拟化

1. 在 Windows 中按 `Ctrl + Shift + Esc` 打开任务管理器。
2. 点击 **性能**。
3. 选择 **CPU**。
4. 查看右下角是否显示 **虚拟化：已启用**。

如果显示 **虚拟化：已禁用**，需要进入 BIOS/UEFI 开启 Intel VT-x、Intel Virtualization Technology、AMD-V 或 SVM Mode。不同品牌电脑入口不同，常见按键是 `F2`、`F10`、`F12`、`Del` 或 `Esc`。

---

## 四、安装 VMware Workstation Pro

### 步骤 1：运行安装程序

1. 打开保存安装包的文件夹，例如 `D:\OSLab\`。
2. 双击 `VMware-Workstation-Full-26H1-25388281.exe`。
3. 如果 Windows 弹出“是否允许此应用对设备进行更改”，点击 **是**。
4. 等待安装向导加载。

### 步骤 2：按向导安装

1. 点击 **Next**。
2. 勾选 **I accept the terms in the License Agreement**，点击 **Next**。
3. 安装位置保持默认即可，点击 **Next**。
4. 如果看到 **Enhanced Keyboard Driver**，可不勾选；普通实验不需要。
5. **Check for product updates on startup** 可取消勾选，避免每次启动检查更新。
6. **Join the VMware Customer Experience Improvement Program** 可取消勾选。
7. 快捷方式保持默认，点击 **Next**。
8. 点击 **Install** 开始安装。
9. 安装完成后点击 **Finish**。

### 步骤 3：首次启动

1. 从桌面或开始菜单打开 **VMware Workstation Pro**。
2. 如果出现许可证或使用类型页面，按学校或教师说明选择。
3. 能看到 VMware 主界面，即表示安装完成。可在 **Help → About VMware Workstation** 中确认版本为教师指定的 26H1。

---

## 五、解压并打开 Kali 预装虚拟机

教师下发的是 Kali 官方**预装好系统的 VMware 虚拟机**，解压后在 VMware 中打开即可使用：不需要新建虚拟机，也不需要走系统安装流程。

### 步骤 1：解压 7z 压缩包

1. 在 Windows 中找到 `kali-linux-2026.2-vmware-amd64.7z`。
2. Windows 11 可直接在资源管理器中右键选择**全部解压缩**；Windows 10 需要先安装 7-Zip（<https://www.7-zip.org/>），再右键 → **7-Zip → 解压到 "kali-linux-2026.2-vmware-amd64\"**。
3. 解压位置选剩余空间充足的磁盘：解压后的虚拟磁盘会随使用增长，建议预留 60GB 以上。

### 步骤 2：在 VMware 中打开并启动

1. 打开 VMware Workstation Pro，点击 **File → Open**。
2. 选择解压目录中的 `kali-linux-2026.2-vmware-amd64.vmx`，点击**打开**，左侧库中会出现这台虚拟机。
3. 点击 **Power on this virtual machine**。VMware 会询问 **This virtual machine might have been moved or copied**，选择 **I Copied It**（VMware 会重新生成这台虚拟机的标识，避免网络冲突）。

### 步骤 3：按档位调整硬件

关闭虚拟机后，选中它并打开 **VM → Settings**，按第三节选定的档位调整：

| 硬件 | 建议值 |
| :--- | :--- |
| Memory | 6144 MB；宿主机只有 8GB 内存时改为 4096MB |
| Processors | 2 个核心 |
| Network Adapter | NAT（保持默认） |

> VMware 可能将 CPU 分成 **Number of processors** 和 **Number of cores per processor** 两项。本课程建议前者设为 `1`，2 核档将后者设为 `2`，4 核档将后者设为 `4`。两者相乘才是 Kali 中 `nproc` 看到的总核心数。
>
> 预装镜像的虚磁盘大小由镜像自带，不小于 40GB 即符合课程要求；需要更大空间时，按下面的「扩容磁盘（选做）」操作。

### 扩容磁盘（选做）

如果 `lsblk` 看到虚磁盘小于 40GB，或想留更多空间：

1. 关闭虚拟机，在 **VM → Settings → Hard Disk → Expand** 中输入更大的上限。
2. 启动 Kali，执行 `lsblk` 确认磁盘总大小已变大，并记下根分区所在磁盘和分区号（例如 `/dev/sda1`）。
3. 执行 `sudo growpart /dev/sda 1`，再执行 `sudo resize2fs /dev/sda1`（两个命令末尾的磁盘和分区号按第 2 步看到的实际值填写），最后用 `df -h /` 确认根分区变大。

---

## 六、首次进入系统：登录、改密码与资源检查

### 步骤 1：登录并修改密码

预装镜像的默认账号：

| 项目 | 默认值 |
| :--- | :--- |
| 用户名 | `kali` |
| 密码 | `kali` |

1. 在登录界面输入用户名 `kali` 和密码 `kali`。
2. 进入桌面后按 `Ctrl + Alt + T` 打开终端，执行 `passwd` 修改密码，按提示输入两遍新密码并牢记。后面的 SSH 远程登录用的就是这个新密码。
3. 系统界面为英文，不需要改成中文——遇到报错、命令输出时，英文更容易搜索和对照。

如果出现黑屏或卡住，先等 2～3 分钟；仍无响应再关闭虚拟机重新启动。

> 预装镜像开箱即用，**不要运行任何安装器**。

### 验收：检查 CPU、内存和存储分配

```bash
nproc
```

输出应与第三节选定的配置档位一致，即 `2` 或 `4`。虚拟机至少应有 2 核。

```bash
free -h
```

看 `Mem` 行的 `total` 列。显示的总内存通常会略小于 VMware 中设置的数值，因为一部分内存被固件和内核占用。虚拟机至少应有 4GB 内存。

```bash
lsblk
```

看虚拟磁盘（通常是 `sda`）的 `SIZE` 列。预装镜像的虚磁盘大小由镜像自带，不小于 40GB 即符合课程要求；需要扩大时见第五节「扩容磁盘（选做）」。

```bash
df -h /
```

看 `Size` 和 `Avail` 列。根文件系统容量会略小于磁盘总量，属于正常现象。

| 项目 | 你的填写内容 |
| :--- | :--- |
| 宿主机内存 / CPU 核心 / 存放盘剩余空间 | 24GB / 18 核（Intel Core Ultra 7 251HX）/ C 盘剩余约 186GB |
| 选择的配置档位 | 课程推荐档（宿主机内存不足 32GB，不满足宽裕档，按规则选低一档） |
| 虚拟 CPU 核心数 | 2（`nproc` 输出 2） |
| 虚拟内存 | 6144 MB（`free -h` 显示 total 5.8Gi） |
| 虚磁盘容量 | 80.1 GB（`lsblk` 显示 sda 80.1G） |
| 根分区可用空间 | 59 GB（`df -h /` 显示 Avail 59G） |
| 资源分配是否符合对应档位 | 符合 |

![虚机资源](imgs/lab3_resources.png)

---

## 七、检查 VMware Tools（确保能复制粘贴命令）

Kali 预装虚拟机一般已经自带 VMware Tools（`open-vm-tools`）。进入桌面、打开终端后，**第一件事就是验证它是否正常工作**：验证通过之前，本文档里的命令只能手动敲进虚拟机终端；验证通过之后，Windows 和虚拟机之间就能互相复制粘贴命令和文字，后面各节的长命令直接从本文档复制即可，桌面分辨率也会随窗口自动调整。

### 步骤 1：验证

逐条执行：

```bash
vmware-toolbox-cmd -v
```

期望输出一个版本号，例如 `12.x.x.xxxxx (build-xxxxxxx)`。

```bash
systemctl is-active open-vm-tools
```

期望输出 `active`。

### 步骤 2：没装或没运行时补装

如果上一节提示 `command not found`，或状态不是 `active`，执行：

```bash
sudo apt update
```

提示输密码时直接输入后回车（输入时屏幕不显示任何字符，下同）。

```bash
sudo apt install -y open-vm-tools open-vm-tools-desktop
```

`open-vm-tools` 是基础服务组件，`open-vm-tools-desktop` 提供桌面集成功能（自适应分辨率、双向复制粘贴、文件拖放）。

```bash
sudo reboot
```

重启登录后，回到步骤 1 重新验证。

### 步骤 3：验证复制粘贴和桌面缩放

1. 在 Windows 里复制一段文字，到虚拟机终端里粘贴，确认能贴上。
2. 拖动 VMware 窗口边缘改变窗口大小，Kali 桌面分辨率应自动适配。

> 复制粘贴或分辨率不生效时，按第十四节「问题 3」处理。

---

## 八、检查虚拟机联网

### 第一步：查看 IP 地址

```bash
hostname -I
```

期望输出一个私有 IP 地址，通常以 `192.168`、`172` 或 `10` 开头。

### 第二步：查看默认路由

```bash
ip route
```

期望能看到一行包含 `default via` 的默认路由，说明虚拟机知道该把外网流量发给哪个网关。

### 第三步：测试 IP 联通性

```bash
ping -c 4 223.5.5.5
```

成功说明虚拟机可以通过 NAT 访问外部网络。

### 第四步：测试 DNS 解析

```bash
ping -c 4 mirrors.tuna.tsinghua.edu.cn
```

成功说明 DNS 解析和域名网络访问正常。

这里只是借一个公网域名验证解析，**不要求你更换软件源**：本实验用官方源也可以，只要第五步的 `sudo apt update` 能正常完成就算合格。

> `ping` 默认会一直运行，`-c 4` 表示只发送 4 个包后自动停止。如果忘记加 `-c` 参数，按 `Ctrl + C` 可以随时停止。

### 第五步：确认软件包索引可以更新

```bash
sudo apt update
```

期望看到若干 `Get:` 行，最后显示读取完成，并且没有 `Err:`、`Failed` 或 `Could not resolve` 之类的错误。

> **软件源用官方源或国内镜像站都可以**，本作业不要求更换软件源，也不会因为 `Get:` 行来自官方源而扣分。只有下载明显缓慢或超时的同学，才需要按第十五节附录换成国内镜像站。
>
> 如果所在网络禁止 ping，但 `sudo apt update` 能正常下载软件索引，可将 `sudo apt update` 的成功输出作为联网证据，并在表格中说明情况。

### 验收

| 项目 | 你的填写内容 |
| :--- | :--- |
| 虚拟机 IP 地址 | 192.168.195.129 |
| 网络模式 | NAT |
| ping `223.5.5.5` 是否成功 | 成功（4 个包全部收到，0% 丢包，平均 61ms） |
| ping `mirrors.tuna.tsinghua.edu.cn` 是否成功 | 成功（4 个包全部收到，0% 丢包，平均 211ms） |
| 软件源（官方源 / 已换的镜像站） | 官方源（http://kali.download/kali，仓库代号 kali-rolling） |
| `sudo apt update` 是否成功 | 成功（Fetched 76.0 MB in 2min 40s，无 Err / Failed） |
| 联网是否合格 | 合格 |

![虚拟机联网](imgs/lab3_network.png)

---

## 九、安装并启用 SSH 服务端

预装镜像不一定带 SSH 服务端，先安装再启用（已安装时重复执行无副作用）：

```bash
sudo apt install -y openssh-server
```

装完之后让 SSH 服务开机自启并立即启动：

```bash
sudo systemctl enable --now ssh
```

`enable` 是设置开机自动启动，`--now` 是同时立刻启动，两件事一条命令完成。执行完这一步，22 端口就会进入监听状态。

### 验证

```bash
ssh -V
```

注意这里是大写字母 `V`，查的是 SSH **客户端**的版本，期望输出形如 `OpenSSH_10.x`（版本随滚动更新变化，有版本号即可）。

```bash
ss -lnt | grep ':22'
```

期望看到一行包含 `LISTEN` 和 `:22` 的输出，说明本机正在监听 SSH 的默认端口。`ss` 用来查看套接字状态：`-l` 只看处于监听（LISTEN）的套接字，`-n` 表示直接显示端口数字不做服务名解析，`-t` 表示只看 TCP。

```bash
dpkg-query -W openssh-server
```

期望输出版本号。注意 `ssh` 客户端和 `openssh-server` 服务端不是一回事，能执行 `ssh` 命令不代表本机可以接受 SSH 连接。

> Kali 中 SSH 不一定开机自启：`systemctl is-active ssh` 显示 `inactive` 时，执行 `sudo systemctl enable --now ssh` 再检查端口。判断标准始终以 22 端口是否处于监听为准。

---

## 十、关于软件源（默认不需要修改）

Kali 装好之后默认使用官方软件源（`http.kali.org`，仓库代号为 `kali-rolling`），**本实验不要求更换软件源**。验收里的软件源一栏，用官方源还是国内镜像站都算合格，不影响任何验收项。

只有出现下面两种情况时，才需要换成国内镜像站，做法见文末 **第十五节附录：配置国内软件源（可选）**：

- `sudo apt update` 或 `sudo apt install` 长时间没有进度、下载速度明显很慢；
- 报 `Could not resolve`、`Connection timed out` 之类的网络错误，但第八节的联网检查全部正常。

换源只是加速手段。如果 `apt` 命令一直卡着不动，可以按 `Ctrl + C` 中断（不会损坏系统），换源之后重新执行；万一之后提示 `dpkg` 被中断，先执行 `sudo dpkg --configure -a` 恢复再重试。

---

## 十一、用 MobaXterm 从 Windows 远程登录 Kali

装好 SSH 服务端之后，从 Windows 宿主机用 SSH 客户端 MobaXterm 远程登录这台 Kali 虚拟机。本课程使用免费的 **MobaXterm Home Edition**。

### 步骤 1：查到 Kali 的 IP 地址

在 Kali 的终端中执行：

```bash
hostname -I
```

记下输出中的 IP（例如 `192.168.x.x`）。NAT 模式下 IP 由 DHCP 分配，虚拟机重启后可能变化，连不上时先回 Kali 里重新查一次。

### 步骤 2：安装 MobaXterm

1. 在 Windows 中打开 <https://mobaxterm.mobatek.net/>，下载 **Home Edition**（免费，选择 Installer 版）。
2. 双击安装包，按向导默认安装即可。

### 步骤 3：新建 SSH 会话

1. 打开 MobaXterm，点击左上角 **Session → SSH**。
2. **Remote host** 填 Kali 的 IP，勾选 **Specify username** 并填写 Kali 用户名，端口保持 `22`。
3. 点击 **OK** 保存会话。

### 步骤 4：登录

1. 双击刚建的会话，首次连接会提示保存服务器指纹，点击 **Accept**。
2. 提示输密码时输入你的 Kali 密码（第六节改过的那个）。注意：输入时终端不显示任何字符，直接输完回车即可。

### 步骤 5：确认登录成功

出现远程终端提示符后，依次执行：

```bash
whoami
hostname
hostname -I
```

能看到自己的用户名、Kali 的主机名和 IP 地址，说明「Windows → SSH → Kali」整条链路已经打通。

> **连不上时**：先在 Kali 里执行 `ss -lnt | grep ':22'` 确认 22 端口处于监听（不在监听就执行 `sudo systemctl enable --now ssh`）；再核对 IP 是否变了；最后确认 Windows 能 ping 通虚拟机的 IP。VMware 的 NAT 网络下宿主机可以直接访问虚拟机 IP，不需要额外配置。

### 验收

| 项目 | 你的填写内容 |
| :--- | :--- |
| Kali 的 IP 地址 | 192.168.195.129 |
| 登录用的 Kali 用户名 | kali |
| 是否登录成功 | 是 |
| 远程终端里 `whoami` 的输出 | kali（`hostname` 输出 kali，`hostname -I` 输出 192.168.195.129） |
| 远程登录是否合格 | 合格 |

![MobaXterm 远程登录](imgs/lab3_mobaxterm.png)

---

## 十二、用 VSCode Remote-SSH 连接 Kali

MobaXterm 提供的是终端，VSCode Remote-SSH 则把整个编辑器“搬”到虚拟机上：文件浏览、编辑、集成终端都直接操作远端。后面的实验在虚拟机里查看和编辑文件主要用它。

### 步骤 1：安装 VSCode 和 Remote - SSH 扩展

1. 在 Windows 中安装 Visual Studio Code：<https://code.visualstudio.com/>
2. 打开 VSCode，按 `Ctrl+Shift+X` 打开扩展面板，搜索 **Remote - SSH**（发布者 Microsoft），点击 **Install**。

### 步骤 2：配置 SSH 主机

1. 按 `Ctrl+Shift+P` 打开命令面板，输入并选择 **Remote-SSH: Open SSH Configuration File**，选择 `C:\Users\你的Windows用户名\.ssh\config`。
2. 在文件中写入下面内容，把 IP 和用户名换成自己的（与 MobaXterm 用同一套）：

```text
Host kali-oslab
    HostName 192.168.x.x
    User kali用户名
    Port 22
```

保存后，以后 IP 变了只需要改这里的 `HostName`。

### 步骤 3：连接

1. 按 `Ctrl+Shift+P`，选择 **Remote-SSH: Connect to Host...**，点击 `kali-oslab`。
2. 首次连接会弹出选择平台，选 **Linux**，接受服务器指纹，然后输入 Kali 的密码。
3. 等待 VSCode 自动把 vscode-server 安装到虚拟机，需要一两分钟，期间虚拟机必须能联网。

### 步骤 4：确认连接成功

1. VSCode 左下角显示 **SSH: kali-oslab**。
2. 选择 **File → Open Folder...**，输入 `~` 打开虚拟机里的用户主目录（即 `/home/kali`），再输一次密码。
3. 按 `` Ctrl+` `` 打开集成终端，执行 `uname -a`——输出是 Kali 的 Linux 内核信息，说明这个终端跑在虚拟机里而不是 Windows 上。

> **常见问题**：
> - 连接超时：先用 MobaXterm 试一次登录，确认 SSH 服务端和 IP 都正常，再回来连 VSCode。
> - 提示 `could not establish connection`：多半是虚拟机重启后 IP 变了，更新 config 文件里的 `HostName` 后重连。
> - 每次连接都要输密码：属正常现象。嫌麻烦可以在 MobaXterm 的 **Tools → MobaKeyGen** 生成密钥对做免密登录（选做，不影响本次验收）。
> - 连接卡在 "Setting up SSH Host"：虚拟机网络断了，回到 Kali 确认能上网后重试。

### 验收

| 项目 | 你的填写内容 |
| :--- | :--- |
| 配置的主机别名（如 `kali-oslab`） | kali-oslab |
| 是否连接成功 | 是（窗口标题与左下角状态栏均显示 kali [SSH: kali-oslab]） |
| 能否打开远程文件夹 | 能（已打开 /home/kali，资源管理器中可见远程文件列表） |
| 远程终端里 `uname -a` 的输出 | Linux kali 6.19.14+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.19.14-1+kali1 (2026-05-05) x86_64 GNU/Linux |
| Remote-SSH 是否合格 | 合格 |

![VSCode Remote-SSH](imgs/lab3_vscode_remote.png)

---

## 十三、创建课程基线快照

全部配置完成后，关闭 Kali，在 VMware 中创建一个名为 `Lab3-ready` 的快照。该快照是干净的课程基线：后面实验如果把环境改坏，可以回到这个状态重来。

> 创建快照这一步**不需要截图，也不需要写进报告**。

---

## 十四、常见问题

遇到问题时，不要只反复执行文中的验收命令。先按下面对应小节修复，再回到对应章节重新验证。

### 问题 1：虚拟机没有 IP 或无法联网

1. 关闭虚拟机，在 VMware 的 **VM → Settings → Network Adapter** 中选择 **NAT**，并勾选 **Connected** 和 **Connect at power on**。
2. 启动 Kali 后查看网卡状态：

```bash
nmcli device status
```

3. 如果网卡显示 `disconnected`，先重启 Kali 网络服务：

```bash
sudo systemctl restart NetworkManager
```

4. 再次执行 `hostname -I`、`ip route` 和 `ping -c 4 223.5.5.5`。能 ping IP 但不能 ping 域名时，是 DNS 问题；IP 和域名都不通时，先检查 NAT 和宿主机网络。

### 问题 2：`apt update` 或安装软件失败

- 显示 `Could not resolve`：DNS 或网络未通，先按“问题 1”处理。
- 下载很慢或超时：按第十五节附录换成国内镜像站；官方源能正常下载时不需要换。
- 换成镜像站后显示找不到仓库：Kali 的仓库代号（`Suite`）必须是 `kali-rolling`，并检查镜像地址是否拼错。
- 显示签名验证失败：不要跳过签名检查，用附录里的备份还原，再重新执行。
- 修改软件源后没生效：Kali 的源配置文件是 `/etc/apt/sources.list`（以及 `/etc/apt/sources.list.d/` 下的 `.list` 文件），确认改对了文件。
- 显示 `Could not get lock`：等待另一个 `apt` 任务完成后重试，不要直接删除锁文件。

### 问题 3：VMware Tools 没有安装，或窗口不能自动缩放

Kali 应使用软件源中的 `open-vm-tools`，不需要在 VMware 菜单中挂载旧式 VMware Tools 光盘。先安装服务和桌面集成组件：

```bash
sudo apt update
```

```bash
sudo apt install -y open-vm-tools open-vm-tools-desktop
```

重启服务和虚拟机：

```bash
sudo systemctl restart open-vm-tools
```

```bash
sudo reboot
```

重启登录后验证：

```bash
vmware-toolbox-cmd -v
```

```bash
systemctl is-active open-vm-tools
```

第一条应输出版本号，第二条应输出 `active`。如果仍不能随窗口改变分辨率：

1. 在 VMware 菜单中选择 **View → Autosize → Autofit Guest**。
2. 确认已登录进入 Kali 桌面，而不是停留在登录界面。
3. 执行 `dpkg-query -W open-vm-tools-desktop`，确认桌面组件已安装。
4. 仍有问题时，执行 `sudo apt install --reinstall -y open-vm-tools open-vm-tools-desktop`，然后再次重启。

如果 VMware 菜单中 **Install VMware Tools** 是灰色，但上面两条验证命令正常，不需要处理；Kali 已通过 `open-vm-tools` 提供同等功能。

如果只是复制粘贴或拖放不生效，关闭虚拟机后打开 **VM → Settings → Options → Guest Isolation**，勾选 **Enable copy and paste** 和 **Enable drag and drop**，然后重新启动虚拟机。

### 问题 4：SSH 装好了却连不上，或提示 `Unit ssh.service could not be found`

先确认服务端软件包是否装上——`ssh` 客户端和 `openssh-server` 服务端不是一回事，能执行 `ssh` 命令不代表本机可以接受 SSH 连接：

```bash
dpkg-query -W openssh-server
```

没有输出版本号就补装：

```bash
sudo apt update
```

```bash
sudo apt install -y openssh-server
```

再确认 22 端口是否在监听：

```bash
ss -lnt | grep ':22'
```

Kali 中 SSH 服务默认不一定开机自启，所以 `systemctl is-active ssh` 显示 `inactive` 时，先执行 `sudo systemctl enable --now ssh` 再检查端口；只要能看到 22 端口处于 `LISTEN`，就说明 SSH 服务端已经就绪。

后面从宿主机登录这台虚拟机时，用 `ssh Kali用户名@Kali的IP地址` 连接，密码就是你自己的 Kali 密码（第六节改过的那个）。

### 其他常见问题

| 现象 | 可能原因 | 处理 |
| :--- | :--- | :--- |
| VMware 提示不支持虚拟化 | BIOS/UEFI 中未开启虚拟化 | 开启 Intel VT-x / AMD-V / SVM Mode |
| 创建虚拟机后很卡 | 分配内存太少或宿主机内存不足 | 虚拟机至少分配 4GB；关闭宿主机不必要的程序 |
| 忘记 Kali 密码 | 无法登录或使用 `sudo` | 没有重要数据时，删除虚拟机文件重新解压一份最省时间 |
| 鼠标被虚拟机捕获 | VMware 正常行为 | 按 `Ctrl + Alt` 释放鼠标 |
| 终端里粘贴的 `sudo` 命令卡住 | 在等密码 | 输入密码时终端不显示字符，直接输入后回车即可 |

---

## 十五、附录：配置国内软件源（可选）

**只有下载明显缓慢或超时的同学才需要做这一节。** 官方源能正常下载时，整节跳过即可，不影响 Lab3 的任何验收项。做之前请先确认第八节的联网检查是通的。

### 为什么要做这一步

Kali 默认从官方源（`http.kali.org`，仓库代号 `kali-rolling`）下载软件包。在中国大陆访问官方源经常很慢，甚至连接超时，会导致后面的 `sudo apt update` 和 `sudo apt install` 长时间卡住或直接失败。把软件源换成国内镜像站之后，下载速度通常有明显提升。

本节以**清华大学开源软件镜像站（TUNA）**为例。

### 步骤 1：备份原有配置

Kali 的软件源配置文件是 `/etc/apt/sources.list`，采用传统的一行式格式。先备份：

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

如果后面配置写错了，用这条命令还原：

```bash
sudo cp /etc/apt/sources.list.bak /etc/apt/sources.list
```

### 步骤 2：写入清华镜像源

把下面**整段内容**复制粘贴到终端后按回车。注意要从第一行的 `sudo tee` 一直复制到最后一行的 `EOF`，中间不能漏行：

```bash
sudo tee /etc/apt/sources.list > /dev/null <<'EOF'
deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
EOF
```

说明：

- `kali-rolling` 是 Kali 的仓库代号，所有 Kali 版本都用它，不需要按版本号修改。
- Kali 官方镜像的签名密钥随系统自带（`kali-archive-keyring`），不需要额外配置签名密钥。

### 步骤 3：确认写入的内容

```bash
cat /etc/apt/sources.list
```

输出应与上一步写入的内容一致，源地址指向 `mirrors.tuna.tsinghua.edu.cn`。

### 步骤 4：刷新软件包索引

```bash
sudo apt update
```

正常时输出中的 `Get:` 行都来自 `mirrors.tuna.tsinghua.edu.cn`，最后显示读取完成，并且没有 `Err:`、`Failed` 或 `Could not resolve` 之类的错误。

> Kali 滚动更新频繁，第一次 `sudo apt update` 拉取的索引较大；如果之后执行 `sudo apt full-upgrade`，需要下载的软件包也可能比较多，属正常现象。

### 备用镜像站

如果清华源当时较慢或无法访问，可以把上面命令中的地址换成下面任意一个，其余内容保持不变：

| 镜像站 | 地址 |
| :--- | :--- |
| 清华大学 TUNA | `https://mirrors.tuna.tsinghua.edu.cn/kali` |
| 阿里云 | `https://mirrors.aliyun.com/kali` |
| 中国科学技术大学 | `https://mirrors.ustc.edu.cn/kali` |

---

## 环境验收总结

| 验收项目 | 合格标准 | 你的结论 |
| :--- | :--- | :--- |
| 虚拟机联网 | 具有 IP 和默认路由，IP 联通与 DNS 解析正常 | 合格 |
| 软件源 | `sudo apt update` 成功，没有 `Err` 或 `Failed`（使用官方源或国内镜像站均可） | 合格（官方源） |
| CPU、内存、存储 | 至少 2 核、4GB、40GB，且与宿主机档位匹配 | 合格（2 核 / 5.8Gi / 80.1GB，对应课程推荐档） |
| MobaXterm 远程登录 | 从 Windows 用 MobaXterm 能 SSH 登录 Kali 并在远程终端执行命令 | 合格 |
| VSCode Remote-SSH | VSCode 能通过 Remote-SSH 连接 Kali，打开远程文件夹并在远程终端执行命令 | 合格 |

简要说明你遇到的问题、解决方法，以及当前环境是否可以继续完成后续实验：

> 填写：
>
> 1. 第九节验证时发现 `ss -lnt | grep ':22'` 没有输出、`systemctl is-active ssh` 显示 inactive，说明预装镜像的 SSH 服务端默认没有开机自启。按文档执行 `sudo systemctl enable --now ssh` 后，22 端口正常进入 LISTEN 状态，之后的 MobaXterm 和 VSCode 连接都一次成功。
> 2. 首次执行 `sudo apt update` 需要下载约 76MB 的软件包索引，用官方源耗时约 3 分钟，速度可以接受，因此没有按附录更换国内镜像源。
> 3. 其余各项（VMware 安装、虚拟机硬件调整、VMware Tools 验证、联网检查）均一次通过，没有遇到文档第十四节之外的问题。
>
> 当前环境（Kali 2026.2，2 核 / 6GB 内存 / 80GB 磁盘，SSH 已启用并设置了开机自启，已按第十三节要求创建 `Lab3-ready` 快照）可以继续完成后续实验。

---

## 截图要求

- 截图须清晰，菜单和终端文字可读。
- 终端截图应同时显示完整命令和其输出。
- 一张截图可以包含同一节下的多条命令及其输出，但每条命令和它的输出必须能对应上。
- 截图中应能看到学生自己的虚拟机，不得直接使用他人截图。
- 必须使用电脑自带的截图功能，严禁使用手机拍摄屏幕。
- 所有截图放在 `imgs/` 目录中，文件名与下表一致。

| 截图内容 | 文件名 |
| :--- | :--- |
| IP、默认路由、IP ping、域名 ping 和 `apt update` 成功 | `imgs/lab3_network.png` |
| `nproc`、`free -h`、`lsblk`、`df -h /` 输出 | `imgs/lab3_resources.png` |
| MobaXterm SSH 会话登录成功，能看到远程终端中 `whoami`、`hostname`、`hostname -I` 的输出 | `imgs/lab3_mobaxterm.png` |
| VSCode 通过 Remote-SSH 连接成功（左下角显示 SSH 主机名，打开远程文件夹，远程终端有 `uname -a` 输出） | `imgs/lab3_vscode_remote.png` |

---

## 提交要求

在自己的“学号姓名”文件夹下新建 `Lab3/`，提交填写完整的 `Lab3.md` 和全部 4 张截图：

```text
学号姓名/
└── Lab3/
    ├── Lab3.md
    └── imgs/
        ├── lab3_network.png
        ├── lab3_resources.png
        ├── lab3_mobaxterm.png
        └── lab3_vscode_remote.png
```

> **注意**：`imgs` 全部小写；文件夹名和截图文件名区分大小写，必须与上面完全一致，否则图片引用会失效。
> 文件名里的分隔符是**下划线 `_`**，不是减号 `-`：要写 `lab3_network.png`，不要写成 `lab3-network.png`。
>
> **只提交上面列出的文件。** 本作业只有 `Lab3.md` 和 4 张截图，不需要提交任何其他文件。提交前用 `git status` 确认变更文件只有上面这 5 个。

---

## 截止时间

**2026 年 10 月 23 日 24:00**

按仓库 `README.md` 第 4 节的规则：不晚于 10 月 23 日 24:00（即 23:59:59）创建 PR 并完成最后一次推送不算超时，10 月 24 日 00:00 起新建 PR 或向已有 PR 推送任何修改均算作超时。时间按北京时间计算，并以 GitHub 记录的最后一次推送时间为准。审核未通过的同学请务必在截止前完成修改。

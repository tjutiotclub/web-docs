# Linux环境与终端入门

Linux 既是常用的开发环境，也是许多路由器、开发板、机器人和边缘设备所运行的操作系统。本章从 Linux 的组成开始，完成终端环境确认，并运行第一组命令。

## 学习目标

完成本章后，你应能够：

- 解释 Linux 内核、发行版、桌面环境、终端和 Shell 的关系。
- 根据开发任务选择 WSL、虚拟机、物理机、服务器或开发板环境。
- 读懂 Bash 命令提示符并执行简单命令。
- 查看发行版、内核、CPU 架构、用户名和当前目录。
- 使用补全、历史记录和中断快捷键提高终端操作效率。

---

## 一、Linux是什么

日常所说的“Linux”包含两个层次：Linux 内核和围绕内核组成的完整操作系统。

### 1. Linux内核

内核位于硬件与应用程序之间，负责管理：

- CPU 时间和进程调度
- 内存
- 文件系统
- 网络
- 硬件设备与驱动
- 用户程序访问系统资源的接口

应用程序通常不会直接控制硬件，而是通过内核提供的系统调用和设备接口完成工作。

### 2. Linux发行版

只有内核还不足以形成完整的日常使用环境。发行版将 Linux 内核与命令行工具、软件包管理器、系统服务、开发工具和桌面环境组合在一起。

常见发行版包括：

| 发行版 | 特点 | 常见场景 |
| --- | --- | --- |
| Ubuntu | 文档与软件资源丰富，版本体系清晰 | 学习、开发、服务器 |
| Debian | 稳定、软件包管理成熟 | 服务器、嵌入式系统基础 |
| Fedora | 软件版本较新 | 桌面开发、新技术体验 |
| Arch Linux | 组件选择自由，要求用户理解系统配置 | 深入学习、定制桌面 |

本系列使用 **Ubuntu LTS + Bash** 作为主要示例。大部分基础命令也适用于其他常见发行版；软件安装命令和部分系统配置方法会随发行版变化。

### 3. 内核、发行版与应用程序的关系

```text
用户
  ↓
应用程序和命令行工具
  ↓
系统库与系统服务
  ↓
Linux内核
  ↓
CPU、内存、磁盘、网卡和外设
```

Ubuntu 是 Linux 发行版，Linux 是其中使用的内核。二者不是同一个概念。

---

## 二、终端、Shell和命令

初学 Linux 时，终端、Shell 和命令经常同时出现，但它们承担不同职责。

### 1. 终端

终端是显示文本、接收键盘输入的窗口。Windows Terminal、GNOME Terminal 和 VS Code 集成终端都属于终端程序。

终端本身通常不解释命令，它负责把输入交给 Shell，再显示 Shell 和其他程序产生的输出。

### 2. Shell

Shell 是命令解释器。它读取用户输入，处理变量、通配符、管道和重定向，然后启动相应程序。

常见 Shell 包括：

- Bash
- Zsh
- Fish
- Dash

本系列使用 Bash。Bash 既可以交互式执行命令，也可以运行 `.sh` 脚本。

### 3. 命令行程序

`ls`、`cat`、`gcc` 和 `git` 都是命令行程序。Shell 找到对应程序并启动它们，再把执行结果显示在终端中。

三者的关系可以概括为：

```text
终端接收输入 → Shell解析输入 → 命令行程序执行任务
```

---

## 三、选择学习环境

不同环境适合不同阶段。基础 Shell 命令在这些环境中基本一致，硬件访问、网络结构和系统控制范围则有所不同。

| 环境 | 优点 | 主要限制 | 适合任务 |
| --- | --- | --- | --- |
| WSL | 启动快，与 Windows 文件和工具协作方便 | 部分硬件和底层系统行为与真实 Linux 不同 | 命令练习、编译、脚本 |
| 虚拟机 | 环境完整，可创建快照，适合反复实验 | 占用内存和磁盘，USB 设备需要映射 | 系统管理、网络和开发实验 |
| Linux物理机 | 性能完整，可直接访问硬件 | 安装和分区需要提前规划 | 长期开发、硬件调试 |
| 远程服务器 | 随时远程使用，适合多人共享 | 依赖网络，通常没有本地图形界面 | 编译、部署、服务运行 |
| Linux开发板 | 直接接触 ARM 和真实外设 | 性能与存储有限 | 交叉编译、嵌入式实验 |

### 推荐顺序

1. 使用 WSL 或 Ubuntu 虚拟机完成文件、Shell、权限、进程和编译练习。
2. 使用 SSH 连接服务器，练习远程操作和文件传输。
3. 使用 Linux 开发板完成交叉编译和设备接口实验。

同一名用户可能同时使用多个环境。例如，在 Windows 中编辑代码，在 WSL 中编译，再通过 SSH 将程序上传到 ARM 开发板运行。

---

## 四、搭建Linux学习环境

Windows 用户可以在 WSL2 和 VMware 虚拟机之间选择一条路线。WSL2 安装更快，适合作为日常开发终端；VMware Workstation 提供完整、独立的 Linux 系统，更适合学习启动、磁盘、网络和系统管理。

完成其中一种安装即可继续后续课程。

### 路线A：安装WSL2和Ubuntu

WSL（Windows Subsystem for Linux）允许 Linux 用户空间直接运行在 Windows 中。WSL2 使用真正的 Linux 内核，并通过轻量虚拟化提供系统环境。

微软的官方安装要求为 Windows 11，或 Windows 10 2004 及以上版本（内部版本 19041 及以上）。

#### 第1步：检查Windows版本

按下 `Win + R`，输入：

```text
winver
```

> **图片占位：** Windows“运行”窗口输入 `winver`，以及版本信息窗口。截图中标出版本和操作系统内部版本。

按 Enter 后会显示 Windows 版本和内部版本号。Windows 10 版本过旧时，应先完成系统更新。

#### 第2步：确认CPU虚拟化已启用

打开“任务管理器”，进入“性能 → CPU”，查看“虚拟化”状态。

```text
虚拟化：已启用
```

> **图片占位：** 任务管理器“性能 → CPU”页面，标出右下角的“虚拟化：已启用”。

如果显示“已禁用”，需要进入计算机 BIOS/UEFI，启用对应选项：

- Intel 平台通常称为 Intel Virtualization Technology、VT-x 或 VMX。
- AMD 平台通常称为 SVM Mode 或 AMD-V。

不同主板进入 BIOS/UEFI 的按键和菜单位置不同，应根据计算机或主板型号查询厂商说明。

#### 第3步：查看可安装的Linux发行版

右键单击开始菜单，选择“终端（管理员）”或“PowerShell（管理员）”，执行：

```powershell
wsl --list --online
```

> **图片占位：** 管理员 PowerShell 窗口和 `wsl --list --online` 输出，标出窗口标题中的“管理员”以及 Ubuntu 发行版名称。

该命令列出 WSL 当前支持安装的发行版及其准确名称。

#### 第4步：安装WSL和Ubuntu

执行：

```powershell
wsl --install -d Ubuntu
```

该命令会检查并启用 WSL 所需组件，然后下载、安装并启动 Ubuntu。在当前版本的 WSL 中，安装完成后通常会直接进入 Ubuntu 的首次初始化流程，并在同一个终端窗口中要求创建 Linux 用户名和密码，不需要先重新启动 Windows。

如果系统明确提示必须重启，保存其他程序中的工作并重新启动 Windows；重启后再次打开 Ubuntu，继续首次初始化即可。

如果不需要提前选择发行版，也可以使用微软提供的默认安装命令：

```powershell
wsl --install
```

默认安装通常会同时安装 Ubuntu。

> **图片占位：** `wsl --install -d Ubuntu` 的完整输出，展示 Ubuntu 下载、安装完成后直接进入用户名创建界面的过程。

#### 第5步：完成Ubuntu首次初始化

Ubuntu 安装完成后通常会在当前终端中直接初始化文件系统，并要求创建 Linux 用户：

```text
Enter new UNIX username:
New password:
Retype new password:
```

如果此前因为系统提示而重新启动了 Windows，则从开始菜单打开 Ubuntu，进入同样的初始化流程。

用户名建议使用小写英文字母和数字，不包含空格。输入密码时终端不会显示字符或星号，这是正常的安全行为。

这里创建的是 Ubuntu 内部用户，名称和密码可以与 Windows 账户不同。该用户会成为 WSL 中的默认登录用户，并可以通过 `sudo` 临时执行系统管理命令。

> **图片占位：** Ubuntu 首次启动时创建 UNIX 用户名和密码的终端界面。截图使用示例用户名，不显示真实密码或个人账户信息。

#### 第6步：检查WSL版本

回到 Windows PowerShell，执行：

```powershell
wsl --list --verbose
```

典型输出：

```text
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

`VERSION` 为 `2` 表示当前发行版运行在 WSL2。还可以查看 WSL 整体状态：

```powershell
wsl --status
wsl --version
```

> **图片占位：** `wsl --list --verbose` 输出，框选 Ubuntu 所在行的 `VERSION 2`。

#### 第7步：更新Ubuntu软件包

打开 Ubuntu 终端，执行：

```bash
sudo apt update
sudo apt upgrade -y
```

第一条命令更新软件包索引，第二条命令升级已经安装的软件包。`sudo` 第一次执行时会要求输入刚才创建的 Linux 用户密码。

更新完成后，安装本系列常用的基础工具：

```bash
sudo apt install -y build-essential git curl wget
```

这些软件分别提供基础编译工具、Git、网络请求和文件下载能力。后续工具链章节会详细解释它们的用途。

#### 第8步：理解Windows与WSL的文件位置

WSL 会将 Windows 磁盘挂载到 `/mnt`：

```bash
ls /mnt/c
```

这对应 Windows 的 `C:\`。

Windows 文件管理器可以通过以下地址访问 WSL 文件：

```text
\\wsl$\Ubuntu\home\你的Linux用户名
```

Linux 项目建议放在 WSL 用户主目录中，例如：

```bash
mkdir -p ~/projects
cd ~/projects
```

把需要频繁编译的 Linux 项目放在 `/home/用户名` 下，可以获得更一致的 Linux 权限行为和文件系统性能。需要与 Windows 交换的普通文件可以通过 `/mnt/c` 或 `\\wsl$` 访问。

#### 第9步：验证WSL环境

在 Ubuntu 终端中执行：

```bash
whoami
pwd
cat /etc/os-release
uname -m
gcc --version
git --version
```

所有命令均能正常输出信息，说明 WSL 学习环境已经可用。

#### WSL安装问题排查

**执行 `wsl --install` 只显示帮助信息**

先列出发行版，再明确指定 Ubuntu：

```powershell
wsl --list --online
wsl --install -d Ubuntu
```

**下载进度长时间停留在 0%**

使用微软提供的网络下载选项：

```powershell
wsl --install --web-download -d Ubuntu
```

**WSL组件或内核需要更新**

在管理员 PowerShell 中执行：

```powershell
wsl --update
wsl --shutdown
```

随后重新打开 Ubuntu。

**提示虚拟化相关错误**

检查三个位置：

1. BIOS/UEFI 中已经启用 Intel VT-x 或 AMD-V。
2. 任务管理器显示“虚拟化：已启用”。
3. Windows 功能中的“虚拟机平台”已经启用。

`wsl --install` 通常会自动启用所需 Windows 功能。功能状态变更后需要重新启动系统。

微软官方说明：[安装WSL](https://learn.microsoft.com/windows/wsl/install)和[WSL基本命令](https://learn.microsoft.com/windows/wsl/basic-commands)。

---

### 路线B：使用VMware Workstation安装Ubuntu虚拟机

虚拟机拥有独立的虚拟磁盘、内存、CPU、网卡和操作系统。Ubuntu 在 VMware Workstation 中执行的安装与普通计算机接近，同时不会修改 Windows 的真实磁盘分区。

#### 第1步：准备资源

建议宿主机至少具备：

- 8 GB 内存
- 40 GB 可用磁盘空间
- 支持并已启用硬件虚拟化的 64 位 CPU
- 稳定的网络连接

为 Ubuntu 虚拟机分配的推荐起点：

| 资源 | 推荐值 |
| --- | --- |
| 虚拟CPU | 2核 |
| 内存 | 4 GB |
| 虚拟磁盘 | 30 GB，动态分配 |
| 网络 | NAT |

宿主机配置充足时可以增加内存和 CPU，但不应把全部资源分配给虚拟机。

#### 第2步：下载Ubuntu镜像

进入 [Ubuntu Desktop官方下载页](https://ubuntu.com/download/desktop)，下载带有 LTS 标记的 64 位 ISO 镜像。

ISO 是安装光盘镜像。下载完成后保留 `.iso` 文件，不要解压。

#### 第3步：下载并安装VMware Workstation Pro

VMware Workstation Pro 的官方下载入口位于 Broadcom Support Portal。注册或登录 Broadcom 账户后，进入“My Downloads → Free Software Downloads”，找到 VMware Workstation Pro，接受对应版本的条款并下载 Windows 安装程序。

Broadcom 官方下载说明：[下载VMware Workstation Pro](https://knowledge.broadcom.com/external/article/344595)。

运行安装程序并保留核心组件。VMware 的虚拟网卡和 USB 组件需要安装驱动，Windows 可能弹出驱动安装确认；安装网络驱动时，当前网络连接可能短暂中断。

安装完成后启动 VMware Workstation Pro。

> **图片占位：** Broadcom Support Portal 中 VMware Workstation Pro 的下载位置，标出 Windows 版本下载项和条款确认位置。

> **图片占位：** VMware Workstation Pro 安装向导的组件选择页面，保留推荐默认选项。

#### 第4步：创建虚拟机

在 VMware Workstation Pro 首页选择“Create a New Virtual Machine”，按以下流程创建：

1. 选择 `Typical (recommended)`。
2. 选择 `Installer disc image file (iso)`。
3. 浏览并选中下载的 Ubuntu LTS ISO。
4. 填写虚拟机名称和保存位置。
5. 设置虚拟磁盘容量。

| 项目 | 示例值 |
| --- | --- |
| Virtual machine name | Ubuntu-Lab |
| Location | 空间充足的本地目录 |
| Installer disc image | 刚下载的 Ubuntu ISO |
| Guest operating system | Linux |
| Version | Ubuntu 64-bit |

VMware 识别 Ubuntu ISO 后可能启用 Easy Install，要求提前填写用户名、密码和主机名。用户名应使用小写字母和数字，主机名不要包含空格。

若要观察完整 Ubuntu 图形安装过程，可以在创建虚拟机时选择 `I will install the operating system later`，完成虚拟机创建后再到 `CD/DVD` 设置中挂载 Ubuntu ISO。下面按照手动安装流程继续。

> **图片占位：** VMware 首页“Create a New Virtual Machine”入口。

> **图片占位：** 新建虚拟机向导的 `Typical` 选择页面。

> **图片占位：** ISO 选择页面，标出 `Installer disc image file (iso)` 和文件路径。

> **图片占位：** 虚拟机名称与保存位置页面，示例名称使用 `Ubuntu-Lab`。

#### 第5步：分配硬件资源

设置：

```text
Base Memory：4096 MB
Processors：2
Virtual Hard Disk：30 GB
```

在完成页面点击 `Customize Hardware`，将内存设置为 4 GB、处理器核心设置为 2，并确认网络适配器使用 NAT。虚拟磁盘文件会随着实际使用逐步增长，设置的 30 GB 是最大容量，不会在创建时立即占满全部空间。

> **图片占位：** `Customize Hardware` 界面，分别标出 Memory、Processors、Network Adapter 和 CD/DVD 四项。

#### 第6步：启动并安装Ubuntu

选中新建的虚拟机并点击“启动”。进入 Ubuntu 安装界面后：

1. 选择安装语言。
2. 选择键盘布局。
3. 选择安装 Ubuntu。
4. 选择默认或交互式安装方案。
5. 在虚拟磁盘上安装系统。
6. 选择时区。
7. 创建用户名、计算机名和登录密码。
8. 等待文件复制和系统配置完成。
9. 根据提示重新启动虚拟机。

安装器中的“擦除磁盘并安装 Ubuntu”针对当前虚拟机连接的虚拟磁盘。在本教程新建的虚拟机中，该磁盘不包含 Windows 文件。安装前仍应确认 VMware 中只连接了预期的虚拟磁盘。

重启时若提示移除安装介质，按 Enter 继续。若再次进入安装界面，可以关闭虚拟机，在 `VM → Settings → CD/DVD` 中取消启动时连接 ISO，或改为自动检测后重新启动。

> **图片占位：** Ubuntu 安装器语言选择和“Install Ubuntu”页面。

> **图片占位：** Ubuntu 安装类型页面，标出虚拟机内的“擦除磁盘并安装 Ubuntu”。图片说明必须强调目标是新建的虚拟磁盘。

> **图片占位：** Ubuntu 用户名、计算机名和密码设置页面，使用虚构示例信息。

#### 第7步：登录并更新系统

使用安装时创建的账户登录 Ubuntu，按 `Ctrl + Alt + T` 打开终端，执行：

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential git curl wget
```

升级完成后重新启动：

```bash
sudo reboot
```

#### 第8步：安装或确认open-vm-tools

VMware Tools 用于提供动态分辨率、共享剪贴板和更好的鼠标集成。Ubuntu 推荐使用发行版软件源中的 `open-vm-tools`。

安装桌面版工具：

```bash
sudo apt install -y open-vm-tools open-vm-tools-desktop
sudo reboot
```

重新登录后改变 VMware 窗口大小。如果 Ubuntu 分辨率能够跟随窗口变化，说明显示集成已经工作。

> **图片占位：** 安装 open-vm-tools 后，Ubuntu 桌面随 VMware 窗口自动调整分辨率的效果。

#### 第9步：创建初始快照

完成更新和基础工具安装后，在 VMware 菜单中选择 `VM → Snapshot → Take Snapshot`，创建快照，例如：

```text
名称：Ubuntu基础环境
说明：系统更新完成，已安装基础开发工具
```

后续实验破坏配置时，可以恢复该快照，而不必重新安装系统。快照不能替代重要文件备份，项目代码仍应提交到 Git 或复制到独立存储位置。

> **图片占位：** VMware 的 Take Snapshot 窗口，填写“Ubuntu基础环境”和对应说明。

#### 第10步：验证虚拟机环境

在 Ubuntu 终端中执行：

```bash
whoami
hostname
pwd
cat /etc/os-release
uname -m
gcc --version
ip addr
```

能看到用户、系统、架构、编译器和网络接口信息，说明虚拟机学习环境已经可用。

VMware 官方的新建虚拟机流程：[使用VMware Workstation创建虚拟机](https://knowledge.broadcom.com/external/article/315434)。

#### VMware安装问题排查

**创建虚拟机时没有64位Ubuntu选项**

检查 BIOS/UEFI 硬件虚拟化是否启用，并确认 Windows 任务管理器显示“虚拟化：已启用”。

**虚拟机启动后黑屏或运行缓慢**

关闭虚拟机后检查：

- 内存是否至少分配 4 GB。
- CPU 是否至少分配 2 核。
- 宿主机是否仍保留足够的内存和 CPU 资源。
- 显示设置中的显存是否合理。

**虚拟机无法联网**

关闭虚拟机，在 `VM → Settings → Network Adapter` 中确认网卡已启用，连接方式为 NAT。NAT 足以完成软件安装和普通网络访问。

**分辨率无法随窗口变化**

安装 `open-vm-tools` 和 `open-vm-tools-desktop`，重新启动 Ubuntu 后再次调整窗口大小。

---

### WSL与虚拟机如何选择

| 需求 | 推荐环境 |
| --- | --- |
| 快速学习命令、编译和脚本 | WSL2 |
| 与Windows编辑器和文件协作 | WSL2 |
| 学习完整Linux桌面和系统管理 | VMware Workstation |
| 练习独立虚拟磁盘、启动和网络配置 | VMware Workstation |
| 直接调试嵌入式USB设备 | Linux物理机或确认设备映射后的虚拟机 |
| 验证ARM目标程序 | 对应ARM开发板 |

本系列的文件、Shell、软件包和编译章节可以在 WSL2 或 VMware Workstation 中完成。涉及完整启动流程、磁盘挂载和特定硬件访问时，VMware 虚拟机或真实 Linux 设备更合适。

---

## 五、打开终端

### Ubuntu桌面

在应用程序列表中打开“终端”，也可以使用常见快捷键：

```text
Ctrl + Alt + T
```

### WSL

可以从开始菜单打开已安装的 Linux 发行版，也可以在 Windows Terminal 中选择对应的发行版配置。

### 远程服务器或开发板

远程环境通常通过 SSH 登录：

```bash
ssh 用户名@主机地址
```

SSH 的配置、密钥和文件传输将在“网络与远程连接”一章详细介绍。

打开终端后，通常会看到类似提示符：

```text
student@linux-pc:~$
```

---

## 六、读懂命令提示符

以以下提示符为例：

```text
student@linux-pc:~$
```

各部分含义如下：

| 内容 | 含义 |
| --- | --- |
| `student` | 当前用户名 |
| `@` | 用户名和主机名的分隔符 |
| `linux-pc` | 当前主机名 |
| `:` | 主机名和当前目录的分隔符 |
| `~` | 当前用户的主目录 |
| `$` | 当前为普通用户 |

root 用户的提示符通常以 `#` 结束：

```text
root@linux-pc:~#
```

`#` 表示当前拥有系统最高权限。root 可以修改或删除关键系统文件，因此日常学习应使用普通用户，只在需要系统权限的单条命令前使用 `sudo`。

提示符的样式可以自定义，所以实际显示可能不同。判断身份和目录时，以 `whoami` 和 `pwd` 的结果为准。

---

## 七、命令的基本结构

Linux 命令通常由命令名、选项和参数组成：

```text
命令 [选项] [参数]
```

例如：

```bash
ls -l /home
```

其中：

- `ls` 是命令名，用于列出目录内容。
- `-l` 是选项，要求使用详细格式显示。
- `/home` 是参数，指定需要查看的目录。

方括号在命令说明中表示“可选”，实际输入时不需要写方括号。

Linux 命令和文件名区分大小写：

```text
file.txt
File.txt
FILE.txt
```

这三个名称代表三个不同的文件。

输入命令后按 Enter 执行。命令执行完成时，Shell 会再次显示提示符，等待下一条命令。

---

## 八、确认当前Linux环境

下面的命令只读取系统信息，可以直接执行。

### 1. 查看发行版

```bash
cat /etc/os-release
```

典型输出包含：

```text
NAME="Ubuntu"
VERSION="... LTS (...)"
ID=ubuntu
```

重点关注：

- `NAME`：发行版名称
- `VERSION`：发行版版本
- `ID`：发行版标识

`/etc/os-release` 是文本文件，`cat` 将其内容输出到终端。

### 2. 查看内核版本

```bash
uname -r
```

该命令只显示当前正在运行的内核版本。查看更完整的系统信息可以使用：

```bash
uname -a
```

发行版版本和内核版本是两个独立概念。更新内核不等于更换发行版。

### 3. 查看处理器架构

```bash
uname -m
```

常见结果如下：

| 输出 | 含义 |
| --- | --- |
| `x86_64` | 64位 x86 架构，常见于个人计算机和服务器 |
| `aarch64` | 64位 ARM 架构，常见于新型开发板和服务器 |
| `armv7l` | 32位 ARM 架构，常见于部分嵌入式开发板 |
| `riscv64` | 64位 RISC-V 架构 |

目标架构决定了程序应使用哪一种编译器和二进制格式。交叉编译章节会继续使用该信息。

### 4. 查看当前用户

```bash
whoami
```

输出当前有效用户名，例如：

```text
student
```

### 5. 查看当前目录

```bash
pwd
```

`pwd` 是 print working directory 的缩写。它输出当前工作目录的绝对路径，例如：

```text
/home/student
```

Shell 中的多数文件操作都以当前工作目录为基础，因此执行复制、移动或删除命令前应先确认位置。

### 6. 查看登录Shell

```bash
echo "$SHELL"
```

典型输出：

```text
/bin/bash
```

环境变量 `SHELL` 通常保存当前用户配置的登录 Shell。若要查看当前终端实际运行的 Shell，可以使用：

```bash
ps -p $$ -o comm=
```

其中 `$$` 表示当前 Shell 的进程号。

### 7. 查看主机名

```bash
hostname
```

主机名用于在网络和命令提示符中标识当前设备。实验室中同时操作多台开发板时，应先确认主机名，避免在错误设备上执行命令。

---

## 九、提高终端操作效率

### Tab自动补全

输入命令或路径的一部分后按 Tab，Shell 会尝试补全剩余内容。

- 只有一个匹配项时，直接完成补全。
- 存在多个匹配项时，连续按两次 Tab 可以显示候选项。

补全可以减少输入错误，也能帮助确认文件或命令是否存在。

### 上下方向键

- `↑`：调出上一条历史命令。
- `↓`：向较新的历史命令移动。

修改历史命令后按 Enter，可以重新执行修改后的内容。

### Ctrl+C

```text
Ctrl + C
```

向当前前台程序发送中断信号。命令长时间运行或输入错误导致程序等待时，可以先使用它返回提示符。

### Ctrl+L

```text
Ctrl + L
```

清理当前终端显示，效果与 `clear` 命令相近，不会删除命令历史。

### Ctrl+D

```text
Ctrl + D
```

在空输入位置表示输入结束。在交互式 Shell 中通常会退出当前会话。也可以使用更直观的命令：

```bash
exit
```

### 查看命令历史

```bash
history
```

该命令列出当前 Shell 保存的历史命令。历史记录可能包含路径、主机地址等信息，不应在命令行直接输入密码、令牌或私钥内容。

---

## 十、第一次终端练习

依次执行：

```bash
whoami
hostname
pwd
cat /etc/os-release
uname -r
uname -m
echo "$SHELL"
ps -p $$ -o comm=
```

根据输出填写环境记录：

| 项目 | 当前环境 |
| --- | --- |
| 发行版及版本 |  |
| 内核版本 |  |
| CPU架构 |  |
| 当前用户名 |  |
| 主机名 |  |
| 当前目录 |  |
| 登录Shell |  |
| 当前Shell进程 |  |

然后完成以下操作：

1. 使用 `↑` 调出刚才执行过的命令。
2. 输入 `una` 后按 Tab，尝试补全 `uname`。
3. 执行 `history` 查看命令记录。
4. 使用 `Ctrl+L` 清理屏幕。
5. 再次执行 `pwd`，确认清屏没有改变当前目录。

---

## 十一、常见问题

### 命令提示“command not found”

Shell 没有找到对应命令。依次检查：

1. 命令拼写和大小写。
2. 命令是否已经安装。
3. 可执行文件是否位于 Shell 的搜索路径中。

后续可以使用 `which`、`type` 和软件包管理器进一步定位。

### 输入密码时没有任何显示

终端输入 `sudo` 或 SSH 密码时通常不显示字符，也不会显示星号。完成输入后直接按 Enter。

### WSL中的内核信息包含Microsoft

WSL 使用由 Windows 提供和管理的 Linux 内核环境，因此 `uname` 输出中可能出现 Microsoft 或 WSL 标识。这不影响大多数 Shell、编译和脚本练习。

### 提示符显示`#`

这通常表示当前处于 root Shell。执行以下命令确认：

```bash
whoami
```

若输出为 `root`，可以使用 `exit` 返回上一层普通用户会话。

### 终端中的复制粘贴快捷键不同

许多 Linux 终端使用：

```text
Ctrl + Shift + C  复制
Ctrl + Shift + V  粘贴
```

普通 `Ctrl+C` 用于中断前台程序，因此通常不承担复制功能。

---

## 本章小结

本章建立了后续学习使用的环境模型：发行版在 Linux 内核之上提供完整系统，终端承载交互界面，Shell 解释输入并启动命令行程序。

现在你应能够确认自己正在操作哪一台设备、使用什么发行版和处理器架构、以哪个用户身份运行，以及当前位于文件系统的什么位置。下一章将沿着当前目录继续学习 Linux 的目录树、路径和文件类型。

## 本章检查点

- 能解释 Linux 内核与 Ubuntu 发行版之间的关系。
- 能区分终端、Shell 和命令行程序。
- 能读懂 `student@linux-pc:~$` 的各个组成部分。
- 能查询发行版、内核、架构、用户、主机名和当前目录。
- 能根据任务说明 WSL、虚拟机、服务器和开发板环境的差异。
- 能使用 Tab、历史记录、`Ctrl+C`、`Ctrl+L` 和 `exit` 完成基本终端操作。

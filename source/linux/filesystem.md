# Linux文件系统与路径

Linux 将普通文件、目录、硬件设备和部分内核运行信息组织在同一棵目录树中。理解这棵目录树，是使用命令行、编写程序和操作嵌入式设备的基础。

本章所有示例均在 **WSL2 的 Ubuntu** 中执行。示例用户名统一使用 `student`，实际操作时应以自己的用户名和主目录为准。

## 学习目标

完成本章后，你应能够：

- 理解 Linux 单一目录树的组织方式。
- 区分根目录、用户主目录和当前工作目录。
- 正确使用绝对路径与相对路径。
- 使用 `pwd`、`cd`、`ls`、`mkdir`、`touch` 等命令操作路径和文件。
- 认识普通文件、目录、符号链接、字符设备和块设备。
- 说明 `/home`、`/etc`、`/usr`、`/var`、`/tmp`、`/dev`、`/proc` 和 `/sys` 的用途。
- 理解文件系统、存储设备和挂载点之间的关系。
- 在 WSL 与 Windows 之间正确访问文件。

---

## 一、准备本章练习目录

打开 WSL 中的 Ubuntu 终端，先确认当前用户和所在目录：

```bash
whoami
pwd
```

典型输出：

```text
student
/home/student
```

创建本章专用练习目录：

```bash
mkdir -p ~/linux-course/filesystem
cd ~/linux-course/filesystem
pwd
```

输出应类似：

```text
/home/student/linux-course/filesystem
```

其中：

- `mkdir` 用于创建目录。
- `-p` 表示父目录不存在时一并创建。
- `~` 代表当前用户的主目录。
- `cd` 用于改变当前工作目录。
- `pwd` 用于显示当前工作目录的绝对路径。

本章中的练习文件都放在该目录内，避免影响系统文件和个人项目。

> **图片占位：** WSL Ubuntu 终端中依次执行 `whoami`、`mkdir -p`、`cd` 和 `pwd`，框选最终路径 `/home/用户名/linux-course/filesystem`。

---

## 二、Linux只有一棵目录树

Windows 通常使用盘符区分不同存储位置：

```text
C:\
D:\
E:\
```

Linux 使用一棵从根目录 `/` 开始的目录树。磁盘分区、U 盘、网络文件系统和虚拟文件系统都接入这棵目录树中的某个位置。

```text
/
├── home
│   └── student
├── etc
├── usr
├── var
├── tmp
├── dev
├── proc
├── sys
└── mnt
```

根目录写作：

```text
/
```

它是整棵目录树的起点。以下路径都从根目录开始：

```text
/home/student
/etc/hosts
/usr/bin/gcc
/mnt/c/Users
```

路径中的 `/` 同时承担两个作用：

- 单独出现时表示根目录。
- 出现在路径中时用于分隔各级目录名。

Linux 路径使用正斜杠 `/`，不是 Windows 路径中的反斜杠 `\`。

---

## 三、当前工作目录

Shell 始终在某个目录中运行，这个目录称为当前工作目录。许多相对路径都从这里开始解析。

### 使用pwd查看当前目录

```bash
pwd
```

`pwd` 是 print working directory 的缩写。若当前位于本章练习目录，输出类似：

```text
/home/student/linux-course/filesystem
```

### 使用cd切换目录

进入根目录：

```bash
cd /
pwd
```

返回用户主目录：

```bash
cd ~
pwd
```

也可以直接执行不带参数的 `cd`：

```bash
cd
pwd
```

不带参数的 `cd` 同样返回当前用户的主目录。

回到本章练习目录：

```bash
cd ~/linux-course/filesystem
```

### 使用cd -返回上一次目录

先进入 `/tmp`：

```bash
cd /tmp
```

再执行：

```bash
cd -
```

Shell 会切换回上一次所在目录，并输出对应路径。再次执行 `cd -`，会在两个目录之间来回切换。

这在同时操作源码目录和构建目录时很方便。

---

## 四、绝对路径与相对路径

路径用于描述文件或目录的位置。根据起点不同，路径分为绝对路径和相对路径。

### 1. 绝对路径

绝对路径从根目录 `/` 开始，完整描述目标在整棵目录树中的位置。

例如：

```text
/home/student/linux-course/filesystem
```

无论当前工作目录在哪里，这个路径始终指向同一个位置。

执行：

```bash
cd /home/student/linux-course/filesystem
```

需要把 `student` 替换成自己的用户名。更通用的写法是：

```bash
cd "$HOME/linux-course/filesystem"
```

`$HOME` 保存当前用户主目录的绝对路径。

### 2. 相对路径

相对路径不以 `/` 开头，它以当前工作目录作为起点。

创建目录结构：

```bash
cd ~/linux-course/filesystem
mkdir -p project/src project/include project/build
```

当前目录结构为：

```text
filesystem/
└── project/
    ├── build/
    ├── include/
    └── src/
```

进入 `project`：

```bash
cd project
```

此时下面两个命令指向同一个目录：

```bash
cd src
```

```bash
cd /home/student/linux-course/filesystem/project/src
```

第一个使用相对路径，第二个使用绝对路径。

### 3. 如何选择

- 交互操作时，相对路径通常更短。
- 脚本、配置文件和错误日志需要明确位置时，绝对路径更直观。
- 路径是否正确取决于上下文，不能只看字符串长短。

执行相对路径命令前，应使用 `pwd` 确认当前目录。

---

## 五、路径中的特殊符号

### 1. 根目录 `/`

```bash
cd /
```

切换到整棵 Linux 目录树的起点。

### 2. 当前目录 `.`

一个点表示当前目录：

```bash
cd ~/linux-course/filesystem/project
ls .
```

`ls .` 表示列出当前目录内容。

当前目录符号常用于执行当前目录中的程序：

```text
./program
```

这里的 `./` 表示“当前目录下的”。

### 3. 上级目录 `..`

两个点表示当前目录的父目录：

```bash
cd ~/linux-course/filesystem/project/src
cd ..
pwd
```

输出应为：

```text
/home/student/linux-course/filesystem/project
```

可以连续使用：

```bash
cd ../..
```

这表示连续返回两级目录。

### 4. 用户主目录 `~`

波浪号由 Shell 展开为当前用户的主目录：

```bash
echo ~
```

典型输出：

```text
/home/student
```

因此：

```bash
cd ~/linux-course
```

等价于：

```bash
cd /home/student/linux-course
```

### 5. 上一次目录 `-`

`cd -` 中的短横线代表上一次工作目录。它只能在 `cd` 等理解该参数的命令中使用，不是通用路径符号。

### 特殊符号总结

| 符号 | 含义 | 示例 |
| --- | --- | --- |
| `/` | 根目录或目录分隔符 | `/etc/hosts` |
| `.` | 当前目录 | `./program` |
| `..` | 上级目录 | `cd ..` |
| `~` | 当前用户主目录 | `cd ~/projects` |
| `-` | 上一次工作目录，仅用于特定命令 | `cd -` |

---

## 六、使用ls观察目录

`ls` 用于列出目录内容。

### 基本用法

```bash
cd ~/linux-course/filesystem
ls
```

列出指定目录：

```bash
ls project
```

### 详细格式

```bash
ls -l
```

典型输出：

```text
drwxr-xr-x 5 student student 4096 Sep 28 10:20 project
```

各列依次表示：

1. 文件类型和权限
2. 硬链接数量
3. 所有者
4. 所属用户组
5. 大小
6. 修改时间
7. 名称

权限将在“用户、用户组与文件权限”一章详细学习。本章先关注第一列的第一个字符和最后一列的名称。

### 显示隐藏文件

Linux 中名称以 `.` 开头的文件通常不会被普通 `ls` 显示，例如 `.bashrc`。

```bash
ls -a ~
```

`-a` 表示显示全部条目，包括隐藏文件以及 `.`、`..`。

更常用的组合是：

```bash
ls -la ~
```

选项可以组合，`-la` 等价于 `-l -a`。

隐藏文件没有特殊的“隐藏属性”，它只遵循名称以点开头的约定。很多程序把用户级配置保存在主目录的隐藏文件或隐藏目录中。

### 以易读单位显示大小

```bash
ls -lh
```

`-h` 表示 human-readable，会使用 K、M、G 等单位显示大小。

### 只查看目录本身

```bash
ls -ld project
```

若没有 `-d`，`ls -l project` 会列出 `project` 里面的内容；加入 `-d` 后显示的是 `project` 目录本身的信息。

---

## 七、创建文件与目录

### 创建目录

```bash
cd ~/linux-course/filesystem
mkdir notes
```

一次创建多个目录：

```bash
mkdir docs images output
```

创建多级目录：

```bash
mkdir -p demo/src/module
```

没有 `-p` 时，如果中间的 `demo/src` 不存在，命令会失败。

### 创建空文件

```bash
touch notes/readme.txt
```

查看：

```bash
ls -l notes
```

若文件不存在，`touch` 会创建空文件；若文件已经存在，`touch` 会更新它的时间戳，不会清空原内容。

### 向文件写入一行文本

```bash
echo "Linux filesystem practice" > notes/readme.txt
```

查看内容：

```bash
cat notes/readme.txt
```

输出：

```text
Linux filesystem practice
```

`>` 会覆盖目标文件。管道和重定向将在 Shell 命令章节详细讲解。

---

## 八、Linux文件名与路径规则

### 1. 区分大小写

执行：

```bash
cd ~/linux-course/filesystem
touch demo.txt Demo.txt DEMO.txt
ls demo.txt Demo.txt DEMO.txt
```

这三个名称代表三个不同文件。输入路径时必须保持大小写一致。

### 2. 点开头表示隐藏文件

```bash
touch .project.conf
ls
ls -a
```

普通 `ls` 看不到 `.project.conf`，`ls -a` 可以看到。

### 3. 文件扩展名不是文件类型的决定条件

Linux 不依赖扩展名决定文件能否执行或如何存储。扩展名主要帮助用户和程序识别用途。

创建一个没有扩展名的文本文件：

```bash
echo "hello" > message
file message
```

`file` 会检查文件内容并给出类型判断。

### 4. 文件名可以包含空格

创建带空格的目录：

```bash
mkdir "test data"
```

访问时需要使用引号：

```bash
cd "test data"
```

也可以使用反斜杠转义空格：

```bash
cd test\ data
```

工程目录和源码文件推荐使用英文字母、数字、短横线和下划线，例如：

```text
sensor-driver
build_output
lesson01
```

这样的名称在命令行、脚本和不同工具之间更稳定。

### 5. Tab补全路径

回到练习目录：

```bash
cd ~/linux-course/filesystem
```

输入：

```text
cd pro
```

按 Tab，Shell 会尝试补全为：

```bash
cd project/
```

路径较长时应优先使用 Tab 补全，既能减少输入，也能提前发现路径不存在或拼写错误。

---

## 九、Linux常见目录

进入根目录并查看：

```bash
cd /
ls
```

WSL Ubuntu 会显示一组系统目录。不同系统的具体内容可能不同，但核心用途一致。

| 目录 | 主要用途 | 示例 |
| --- | --- | --- |
| `/home` | 普通用户主目录 | `/home/student` |
| `/root` | root 用户主目录 | `/root` |
| `/etc` | 系统和服务配置 | `/etc/hosts` |
| `/usr` | 程序、库、头文件和共享资源 | `/usr/bin/gcc` |
| `/var` | 日志、缓存和持续变化的数据 | `/var/log` |
| `/tmp` | 临时文件 | `/tmp/test.txt` |
| `/dev` | 设备文件 | `/dev/null` |
| `/proc` | 进程和内核运行信息 | `/proc/cpuinfo` |
| `/sys` | 设备、驱动和内核对象信息 | `/sys/class` |
| `/mnt` | 常用挂载位置 | `/mnt/c` |
| `/media` | 桌面系统自动挂载可移动设备的常用位置 | `/media/student/...` |
| `/boot` | 启动相关文件 | 内核和引导配置 |
| `/opt` | 附加的第三方软件 | `/opt/application` |

### `/home`与`/root`

普通用户的个人文件存放在 `/home/用户名`。root 用户的主目录是 `/root`，它不位于 `/home` 下。

```bash
echo "$HOME"
```

普通用户的输出类似：

```text
/home/student
```

### `/etc`

`/etc` 保存系统范围的配置。查看主机名解析文件：

```bash
cat /etc/hosts
```

普通用户通常可以读取许多配置，但修改系统配置往往需要管理员权限。

### `/usr`

`/usr` 保存大量用户空间程序、库、头文件和共享数据。例如：

```bash
ls -l /usr/bin/gcc
```

编译工具和开发库通常安装在 `/usr/bin`、`/usr/lib` 和 `/usr/include` 等位置。

### `/var`

`/var` 保存运行期间经常变化的数据，例如日志、缓存和软件包状态。

```bash
ls /var/log
```

排查系统服务问题时，日志通常是重要依据。

### `/tmp`

`/tmp` 用于临时文件。系统或程序可能定期清理其中内容，因此重要数据不应长期保存在这里。

```bash
touch /tmp/linux-course-test.txt
ls -l /tmp/linux-course-test.txt
```

完成后删除该测试文件：

```bash
rm /tmp/linux-course-test.txt
```

---

## 十、认识Linux文件类型

Linux 中“文件”是一个广义概念。普通数据、目录、链接和设备接口都以文件系统对象出现。

### 使用ls -l判断类型

`ls -l` 输出第一列的第一个字符表示类型：

| 字符 | 类型 |
| --- | --- |
| `-` | 普通文件 |
| `d` | 目录 |
| `l` | 符号链接 |
| `c` | 字符设备 |
| `b` | 块设备 |
| `p` | 命名管道 |
| `s` | 套接字 |

执行：

```bash
ls -ld /etc /etc/hosts /dev/null
```

输出开头通常分别是：

```text
d ... /etc
- ... /etc/hosts
c ... /dev/null
```

说明 `/etc` 是目录，`/etc/hosts` 是普通文件，`/dev/null` 是字符设备。

### 使用file判断内容类型

```bash
file /etc/hosts
file /usr/bin/ls
file ~/linux-course/filesystem/notes/readme.txt
```

`file` 根据文件内容和结构判断类型，而不是只看扩展名。

### 使用stat查看完整信息

```bash
stat ~/linux-course/filesystem/notes/readme.txt
```

`stat` 会显示：

- 文件大小
- inode 编号
- 权限
- 所有者和用户组
- 访问、修改和状态变更时间

这些信息将在权限和链接部分继续使用。

---

## 十一、设备文件与虚拟文件系统

### 1. `/dev`：设备接口

`/dev` 中的条目由系统用于表示设备或特殊数据通道。

查看几个常见条目：

```bash
ls -l /dev/null /dev/zero /dev/random
```

- `/dev/null`：丢弃写入的数据，读取时立即返回结束。
- `/dev/zero`：读取时持续产生零字节。
- `/dev/random`：提供随机数据。

嵌入式 Linux 开发板上还可能出现：

```text
/dev/ttyS0
/dev/ttyUSB0
/dev/ttyACM0
/dev/i2c-0
/dev/spidev0.0
```

这些名称分别可能对应串口、USB 转串口、USB CDC 串口、I2C 控制器和用户空间 SPI 设备。设备节点是否存在，取决于硬件、内核驱动和系统配置。

WSL 对 Windows USB 设备的访问需要额外连接步骤，因此本章只观察 WSL 当前已有的 `/dev` 内容。开发板设备节点将在嵌入式 Linux 实践中操作。

### 2. `/proc`：进程与内核运行信息

`/proc` 是由内核动态提供的虚拟文件系统。它不把普通文件永久存储到磁盘中。

查看 CPU 信息：

```bash
cat /proc/cpuinfo
```

查看内存信息：

```bash
head /proc/meminfo
```

查看当前 Shell 的进程信息：

```bash
echo $$
ls -l /proc/$$
```

`$$` 会被 Shell 替换为当前 Shell 的 PID，因此 `/proc/$$` 指向当前 Shell 对应的进程目录。

### 3. `/sys`：设备与内核对象

`/sys` 同样是内核提供的虚拟文件系统，主要按照设备、驱动、总线和类别组织信息。

```bash
ls /sys
ls /sys/class
```

在真实 Linux 开发板上，GPIO、LED、网络接口、存储设备等信息可能通过 `/sys` 中的子系统呈现。

### 4. 为什么它们看起来像文件

Linux 使用统一的文件接口表达多种资源。用户程序可以通过 `open`、`read`、`write`、`close` 等相似操作访问普通文件和许多设备接口。

这形成了常见的 Linux 思想：

```text
一切皆文件
```

它是一种统一接口的设计思路，不表示所有对象都以普通数据文件形式存储在磁盘中。

---

## 十二、符号链接与硬链接

链接让多个路径名称关联到文件系统中的目标。

### 1. 创建符号链接

回到练习目录：

```bash
cd ~/linux-course/filesystem
```

为笔记文件创建符号链接：

```bash
ln -s notes/readme.txt readme-link
ls -l readme-link
```

输出类似：

```text
lrwxrwxrwx ... readme-link -> notes/readme.txt
```

开头的 `l` 表示符号链接，箭头右侧是链接保存的目标路径。

读取链接：

```bash
cat readme-link
```

实际读取的是 `notes/readme.txt`。

### 2. 符号链接可以指向目录

```bash
ln -s project/src source
cd source
pwd
```

符号链接 `source` 指向 `project/src`。这种方式常用于为版本目录、工具链或部署目录提供稳定入口。

### 3. 相对目标与绝对目标

上面的链接保存的是相对路径：

```text
notes/readme.txt
```

相对目标以符号链接所在目录作为起点解析。也可以创建使用绝对路径的链接：

```bash
ln -s "$HOME/linux-course/filesystem/notes/readme.txt" readme-absolute
```

相对链接便于整体移动目录，绝对链接则明确指向系统中的固定位置。

### 4. 目标不存在时

符号链接可以存在，但目标可能已经移动或删除。此时它会成为失效链接。

查看链接保存的目标：

```bash
readlink readme-link
```

解析到最终绝对路径：

```bash
readlink -f readme-link
```

### 5. 硬链接

创建硬链接：

```bash
ln notes/readme.txt readme-hard
ls -li notes/readme.txt readme-hard
```

`-i` 会显示 inode 编号。两个名称具有相同 inode，表示它们引用同一个文件系统对象。

符号链接和硬链接的主要区别：

| 特性 | 符号链接 | 硬链接 |
| --- | --- | --- |
| 保存内容 | 目标路径 | 同一 inode 的另一个名称 |
| 可跨文件系统 | 可以 | 不可以 |
| 可指向目录 | 可以 | 普通用户通常不创建目录硬链接 |
| 目标名称删除后 | 链接可能失效 | 其他硬链接仍可访问数据 |
| `ls -l` 类型 | `l` | 与普通文件相同 |

日常工程中更常使用符号链接。硬链接有助于理解 inode、文件名与文件数据之间的关系。

---

## 十三、文件系统与挂载点

### 1. 文件系统是什么

文件系统规定数据如何在存储介质上组织、命名和记录。常见 Linux 文件系统包括 ext4、XFS 和 Btrfs；Windows 常见 NTFS。

一个磁盘可以包含多个分区，每个分区可以保存一个文件系统。Linux 通过“挂载”将文件系统接入现有目录树。

### 2. 挂载点是什么

假设一个存储设备上的文件系统被挂载到：

```text
/mnt/data
```

挂载完成后，访问 `/mnt/data` 就是在访问该文件系统的根目录。

```text
Linux目录树
/
└── mnt
    └── data  ← 另一个文件系统的挂载点
```

Linux 不需要为每个设备分配新的盘符，设备通过挂载点进入统一目录树。

### 3. 查看当前挂载关系

```bash
findmnt
```

`findmnt` 以树状结构显示文件系统和挂载点。WSL2 中可以看到 Linux 根文件系统以及 Windows 磁盘对应的挂载项。

只查看 Windows C 盘对应位置：

```bash
findmnt /mnt/c
```

### 4. 查看文件系统空间

```bash
df -h
```

`df` 显示各文件系统的总容量、已用空间、可用空间和挂载点；`-h` 使用易读单位。

查看某个路径所在文件系统：

```bash
df -h ~
df -h /mnt/c
```

这两个路径可能属于不同的文件系统。

### 5. 查看块设备

```bash
lsblk
```

`lsblk` 用于列出块设备、分区和挂载点。WSL2 的虚拟磁盘呈现方式与普通物理 Linux 主机不同，因此输出内容会少于真实开发板或服务器，但列名和读取方法相同。

本章只查看挂载状态，不执行手动挂载或卸载。后续需要连接磁盘镜像、开发板存储卡或 U 盘时，再根据明确的设备名称进行操作。

---

## 十四、WSL与Windows文件互访

WSL2 同时提供两种常用文件位置：Linux 文件系统和挂载到 `/mnt` 下的 Windows 文件系统。

### 1. 在WSL中访问Windows文件

Windows 的 C 盘通常位于：

```text
/mnt/c
```

列出 Windows 用户目录：

```bash
ls /mnt/c/Users
```

进入当前 Windows 用户的桌面时，路径可能类似：

```bash
cd /mnt/c/Users/Windows用户名/Desktop
```

Windows 用户名和桌面实际位置因账户、语言及 OneDrive 配置而异，应先使用 `ls` 逐级确认。

其他盘符采用相同规则，例如 D 盘通常为：

```text
/mnt/d
```

### 2. 在Windows中访问WSL文件

在 Windows 文件资源管理器地址栏输入：

```text
\\wsl$
```

选择 Ubuntu 后，可以进入：

```text
\\wsl$\Ubuntu\home\Linux用户名
```

> **图片占位：** Windows 文件资源管理器打开 `\\wsl$\Ubuntu\home\用户名`，标出与 WSL 中 `~` 对应的目录。

### 3. 从WSL打开资源管理器

在 WSL 终端的练习目录中执行：

```bash
cd ~/linux-course/filesystem
explorer.exe .
```

Windows 文件资源管理器会打开当前 WSL 目录。命令末尾的 `.` 表示当前目录。

> **图片占位：** 左侧为 WSL 终端执行 `explorer.exe .`，右侧为打开的 Windows 文件资源管理器，展示二者指向同一目录。

### 4. 转换Windows与Linux路径

将 Windows 路径转换为 WSL 路径：

```bash
wslpath 'C:\Users\Public'
```

典型输出：

```text
/mnt/c/Users/Public
```

将 WSL 路径转换为 Windows 路径：

```bash
wslpath -w ~/linux-course/filesystem
```

输出会是可供 Windows 程序使用的路径。

### 5. 项目应该放在哪里

需要在 Linux 中频繁编译、运行脚本或使用 Linux 权限的项目，建议放在 WSL 用户主目录：

```text
/home/用户名/projects
```

需要由 Windows 程序直接管理的大型普通文件，可以保存在 `/mnt/c`、`/mnt/d` 等位置。

在同一项目中保持统一的路径环境，可以减少权限、换行符、路径格式和文件系统性能差异带来的问题。

---

## 十五、路径操作的安全习惯

文件操作命令会直接作用于解析后的目标路径。养成以下习惯可以避免误操作：

### 1. 先确认当前位置

```bash
pwd
```

### 2. 再确认目标内容

```bash
ls -la 目标路径
```

### 3. 使用Tab补全

补全可以验证路径存在，并减少拼写错误。

### 4. 给包含空格的路径加引号

```bash
cd "/mnt/c/Users/Public/My Project"
```

### 5. 不以root身份完成普通文件练习

本章所有练习都应在普通用户主目录中完成，不需要 `sudo`。

### 6. 区分相对路径的起点

同一个相对路径在不同工作目录下会指向不同位置。复制、移动或删除文件前，先执行 `pwd`。

---

## 十六、综合实践

### 实践目标

建立一个小型 C 项目目录，分别使用绝对路径、相对路径和符号链接访问它，并确认它所在的文件系统。

### 第1步：创建目录结构

```bash
cd ~/linux-course/filesystem
mkdir -p sensor-demo/src sensor-demo/include sensor-demo/build sensor-demo/docs
```

创建文件：

```bash
touch sensor-demo/src/main.c
touch sensor-demo/include/sensor.h
echo "Sensor demo documentation" > sensor-demo/docs/readme.txt
```

### 第2步：使用相对路径访问

```bash
cd sensor-demo/src
pwd
ls ../include
cat ../docs/readme.txt
```

回答：

1. 当前目录的绝对路径是什么？
2. `../include` 中的 `..` 指向哪里？
3. 从 `src` 到 `docs/readme.txt` 为什么需要先返回上一级？

### 第3步：创建符号链接

```bash
cd ~/linux-course/filesystem/sensor-demo
ln -s docs/readme.txt README
ls -l README
cat README
```

使用 `readlink` 查看链接目标：

```bash
readlink README
readlink -f README
```

### 第4步：检查文件类型

```bash
file src/main.c
file README
stat docs/readme.txt
```

观察普通文件、符号链接和 inode 信息。

### 第5步：确认文件系统

```bash
df -h ~/linux-course/filesystem/sensor-demo
findmnt -T ~/linux-course/filesystem/sensor-demo
```

`findmnt -T` 会查找指定路径所在的文件系统和挂载点。

### 第6步：从Windows打开项目目录

```bash
cd ~/linux-course/filesystem/sensor-demo
explorer.exe .
```

在 Windows 文件资源管理器中确认 `src`、`include`、`build` 和 `docs` 目录均存在。

> **图片占位：** WSL 中的 `sensor-demo` 项目结构与 Windows 文件资源管理器中的同一目录并排展示。

---

## 十七、常见问题

### `cd`提示No such file or directory

表示 Shell 无法按当前路径找到目标。依次检查：

1. 执行 `pwd` 确认相对路径起点。
2. 执行 `ls` 查看实际名称。
3. 检查大小写。
4. 对路径使用 Tab 补全。
5. 路径含空格时使用引号。

### `ls`看不到刚创建的隐藏文件

使用：

```bash
ls -la
```

名称以 `.` 开头的文件默认不会出现在普通 `ls` 输出中。

### Windows路径复制到WSL后无法使用

Windows 路径：

```text
C:\Users\Public\Documents
```

对应 WSL 路径通常为：

```text
/mnt/c/Users/Public/Documents
```

也可以交给 `wslpath` 转换：

```bash
wslpath 'C:\Users\Public\Documents'
```

### `~`为什么有时没有被展开

`~` 的展开由 Shell 完成。它必须出现在路径开头的合适位置。以下写法有效：

```bash
cd ~/projects
```

把它放入双引号后不会按预期展开：

```bash
echo "~/projects"
```

需要在引号中构造主目录路径时，使用 `$HOME`：

```bash
echo "$HOME/projects"
```

### 符号链接显示为红色或无法打开

通常表示链接目标不存在。检查：

```bash
ls -l 链接名称
readlink 链接名称
readlink -f 链接名称
```

确认目标是否被移动、删除，或相对链接的起点是否理解错误。

### `/proc`中的文件大小看起来不正常

`/proc` 是内核动态生成的虚拟文件系统。目录项显示的大小不一定代表读取时能够获得的数据量，也不对应普通磁盘占用。

---

## 本章小结

Linux 使用从 `/` 开始的单一目录树组织系统资源。绝对路径从根目录开始，相对路径从当前工作目录开始；`.`、`..`、`~` 和 `cd -` 分别用于表示当前目录、上级目录、用户主目录和上一次工作目录。

`/home` 保存普通用户文件，`/etc` 保存系统配置，`/usr` 保存程序和开发资源，`/var` 保存变化数据。`/dev`、`/proc` 和 `/sys` 将设备与内核运行信息纳入文件接口。文件系统通过挂载点接入目录树，WSL 则将 Windows 磁盘挂载到 `/mnt/c`、`/mnt/d` 等位置。

理解路径的起点、文件类型和挂载关系后，下一章中的复制、移动、搜索、管道和重定向才有明确的操作对象。

---

## 本章检查点

- 能解释根目录 `/`、主目录 `~` 和当前目录 `.` 的区别。
- 能为同一文件写出绝对路径和相对路径。
- 能使用 `pwd`、`cd`、`ls`、`mkdir`、`touch` 和 `file`。
- 能读懂 `ls -l` 输出中的文件类型字符。
- 能说明 `/home`、`/etc`、`/usr`、`/var` 和 `/tmp` 的用途。
- 能解释 `/dev`、`/proc`、`/sys` 为什么不等同于普通磁盘目录。
- 能创建并检查符号链接。
- 能解释文件系统挂载到目录的含义。
- 能在 WSL 中访问 Windows 磁盘，并从 Windows 打开 WSL 主目录。
- 能说明为什么 Linux 项目适合保存在 WSL 用户主目录中。

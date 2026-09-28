# 用户、用户组与文件权限

Linux 是多用户系统。内核根据进程身份、文件所有者、所属用户组和权限位决定一次访问是否允许。本章从身份模型开始，逐步掌握 `rwx`、`chmod`、`chown`、`umask`、`sudo` 和常见权限故障排查。

本章所有示例均在 **WSL2 的 Ubuntu** 中执行。实验文件统一放在当前用户主目录中。

## 学习目标

完成本章后，你应能够：

- 理解用户名、UID、用户组、GID、主用户组和附加用户组。
- 读懂 `ls -l` 输出中的文件类型、所有者、所属组和权限位。
- 解释 `r`、`w`、`x` 对普通文件和目录的不同作用。
- 使用符号表示和数字表示修改权限。
- 使用 `chown` 与 `chgrp` 修改所有者和所属组。
- 理解新文件权限与 `umask` 的关系。
- 正确使用 `sudo` 执行需要管理员权限的单条命令。
- 理解 setuid、setgid 和 sticky bit 的用途。
- 判断串口设备访问是否受用户组限制。
- 按步骤排查 `Permission denied`。

---

## 一、准备练习环境

打开 WSL Ubuntu 终端，创建本章练习目录：

```bash
mkdir -p ~/linux-course/permission
cd ~/linux-course/permission
pwd
```

输出类似：

```text
/home/student/linux-course/permission
```

创建几个初始文件：

```bash
printf "public information\n" > public.txt
printf "private information\n" > private.txt
mkdir -p project
printf "project configuration\n" > project/config.txt
```

查看：

```bash
ls -la
ls -la project
```

> **图片占位：** WSL 终端中创建 `permission` 练习目录，并显示 `ls -la` 输出。标出所有者、所属组和权限列。

---

## 二、Linux如何表示用户身份

### 1. 用户名与UID

人通常使用用户名识别账户：

```text
student
root
```

内核主要使用数值 UID（User ID）识别用户。用户名是方便人阅读的名称，系统通过账户数据库建立用户名与 UID 的对应关系。

查看当前用户名：

```bash
whoami
```

查看完整身份：

```bash
id
```

典型输出：

```text
uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)
```

其中：

| 内容 | 含义 |
| --- | --- |
| `uid=1000(student)` | 当前用户的 UID 和用户名 |
| `gid=1000(student)` | 当前用户的主用户组 GID 和组名 |
| `groups=...` | 当前用户所属的全部用户组 |

不同系统分配的数字可能不同，不应假定普通用户永远是 UID 1000。

只查看 UID：

```bash
id -u
```

只查看主用户组 GID：

```bash
id -g
```

### 2. root用户

root 是系统管理员账户，UID 固定为 `0`。它可以访问和修改大多数系统资源，也可以更改其他文件的所有者和权限。

```text
普通用户：完成日常学习和开发
root用户：执行系统管理操作
```

日常工作使用普通用户，需要系统权限时通过 `sudo` 执行明确的单条命令，可以缩小误操作范围。

### 3. 系统用户

Linux 还包含许多用于运行服务的系统用户，例如数据库、Web 服务和日志服务账户。它们让不同服务以不同身份运行，从而限制单个服务能够访问的资源。

系统用户通常不用于交互登录，但仍有独立 UID、所属组和文件权限。

---

## 三、用户组

用户组让多个用户共享同一组资源权限。

### 1. 主用户组

每个用户有一个主用户组。用户创建普通文件时，文件通常继承当前进程的有效用户身份和默认组规则。

查看当前用户主组名称：

```bash
id -gn
```

### 2. 附加用户组

一个用户还可以属于多个附加用户组。附加组常用于授予特定资源访问能力，例如：

| 用户组 | 常见用途 |
| --- | --- |
| `sudo` | 允许通过 sudo 执行管理命令 |
| `dialout` | 访问串口设备 |
| `docker` | 访问 Docker 服务接口 |
| `video` | 访问部分视频设备 |
| `plugdev` | 访问部分可插拔设备 |

查看当前用户所属组：

```bash
groups
```

也可以查看指定用户：

```bash
groups "$USER"
```

### 3. 用户组不是权限本身

加入某个组只表示用户获得该组身份。真正能否访问文件，还取决于：

- 文件是否属于该组。
- 组权限位是否允许对应操作。
- 路径中各级目录是否允许通过。
- 是否存在 ACL、只读挂载等额外限制。

---

## 四、账户信息保存在哪里

Linux 使用多个系统文件记录账户信息。

### `/etc/passwd`

查看当前用户条目：

```bash
getent passwd "$USER"
```

输出格式类似：

```text
student:x:1000:1000:Student:/home/student:/bin/bash
```

各字段由冒号分隔：

```text
用户名:密码占位:UID:GID:说明:主目录:登录Shell
```

`/etc/passwd` 需要允许普通程序读取用户与 UID 的对应关系，因此密码哈希不直接保存在这里。

### `/etc/shadow`

密码哈希和密码有效期信息保存在权限更严格的 `/etc/shadow`。普通用户不能直接读取它。

### `/etc/group`

查看某个用户组：

```bash
getent group sudo
```

典型字段：

```text
组名:密码占位:GID:附加成员列表
```

使用 `getent` 比直接搜索文件更通用，因为系统账户信息还可能来自网络目录服务。

---

## 五、读懂ls -l权限信息

执行：

```bash
cd ~/linux-course/permission
ls -l public.txt
```

典型输出：

```text
-rw-r--r-- 1 student student 19 Sep 28 10:00 public.txt
```

各部分含义：

```text
-rw-r--r--  1  student  student  19  Sep 28 10:00  public.txt
│└┬┘└┬┘└┬┘     │        │
│ │  │  │      │        └── 所属用户组
│ │  │  │      └─────────── 所有者
│ │  │  └────────────────── 其他用户权限
│ │  └───────────────────── 用户组权限
│ └──────────────────────── 所有者权限
└────────────────────────── 文件类型
```

### 1. 文件类型字符

第一个字符表示对象类型：

| 字符 | 类型 |
| --- | --- |
| `-` | 普通文件 |
| `d` | 目录 |
| `l` | 符号链接 |
| `c` | 字符设备 |
| `b` | 块设备 |
| `p` | 命名管道 |
| `s` | 套接字 |

### 2. 三组权限

后面九个字符每三个为一组：

```text
rw-  r--  r--
│    │    └── other：其他用户
│    └─────── group：所属组成员
└──────────── owner：所有者
```

### 3. 权限不是叠加判断

内核会根据访问者身份选择一组权限：

1. 有效 UID 与文件所有者一致，使用 owner 权限。
2. 否则，只要有效组身份匹配文件所属组，使用 group 权限。
3. 否则，使用 other 权限。

不会先检查 owner，不够时再叠加 group 和 other。命中哪一类，就使用对应的三个权限位。

---

## 六、r、w、x对普通文件的意义

对于普通文件：

| 权限 | 含义 |
| --- | --- |
| `r` | 读取文件内容 |
| `w` | 修改或覆盖文件内容 |
| `x` | 将文件作为程序直接执行 |

### 1. 读取权限

查看当前权限：

```bash
ls -l private.txt
```

移除所有者读取权限：

```bash
chmod u-r private.txt
```

尝试读取：

```bash
cat private.txt
```

会得到 `Permission denied`。恢复权限：

```bash
chmod u+r private.txt
```

### 2. 写入权限

移除所有者写权限：

```bash
chmod u-w private.txt
```

尝试追加：

```bash
echo "new line" >> private.txt
```

Shell 无法打开文件进行写入。恢复：

```bash
chmod u+w private.txt
```

### 3. 执行权限

创建脚本：

```bash
printf '#!/usr/bin/env bash\nprintf "permission demo\\n"\n' > demo.sh
```

查看权限：

```bash
ls -l demo.sh
```

新文件通常没有执行权限。直接运行：

```bash
./demo.sh
```

会得到权限错误。添加所有者执行权限：

```bash
chmod u+x demo.sh
./demo.sh
```

输出：

```text
permission demo
```

使用解释器显式读取脚本：

```bash
bash demo.sh
```

这种方式由 Bash 读取脚本内容，脚本文件本身不依赖直接执行权限，但调用者仍需要读取权限。

---

## 七、r、w、x对目录的意义

目录权限的含义与普通文件不同。

| 权限 | 对目录的意义 |
| --- | --- |
| `r` | 读取目录项名称列表 |
| `w` | 在目录中创建、删除或重命名条目 |
| `x` | 穿过目录并访问已知名称对应的对象 |

### 1. 执行权限是“通过目录”

创建练习目录：

```bash
mkdir -p access-demo
printf "inside directory\n" > access-demo/info.txt
chmod 600 access-demo
```

此时目录所有者拥有 `rw-`，但没有 `x`。尝试访问内部文件：

```bash
cat access-demo/info.txt
```

会得到 `Permission denied`，因为路径解析需要穿过 `access-demo`。

恢复目录权限：

```bash
chmod 700 access-demo
cat access-demo/info.txt
```

### 2. 删除文件取决于父目录

删除一个文件，本质上是修改父目录中的名称记录。因此，能否删除文件主要取决于父目录的 `w` 和 `x` 权限，而不是文件自身的 `w` 权限。

这解释了一个常见现象：只读文件仍可能被其父目录的有权限用户删除。

### 3. 常见目录权限

```text
700  只有所有者能够列出、进入和修改
750  所有者完全访问，组成员可以列出和进入
755  所有者完全访问，其他用户可以列出和进入
770  所有者和组成员完全访问
```

---

## 八、chmod符号表示

`chmod` 用于修改权限位。

符号表示由三部分组成：

```text
对象 + 操作 + 权限
```

### 1. 对象

| 字符 | 对象 |
| --- | --- |
| `u` | user，所有者 |
| `g` | group，所属组 |
| `o` | others，其他用户 |
| `a` | all，所有三类 |

### 2. 操作

| 字符 | 作用 |
| --- | --- |
| `+` | 添加权限 |
| `-` | 移除权限 |
| `=` | 设置为明确权限，覆盖该类原权限 |

### 3. 示例

给所有者添加执行权限：

```bash
chmod u+x demo.sh
```

移除组和其他用户的写权限：

```bash
chmod go-w public.txt
```

将组权限设置为只读：

```bash
chmod g=r public.txt
```

给所有用户添加读取权限：

```bash
chmod a+r public.txt
```

一次设置多组权限：

```bash
chmod u=rw,g=r,o= private.txt
```

结果：

```text
-rw-r-----
```

### 4. 大写X

大写 `X` 只在目标是目录，或文件原本已有某类执行权限时添加执行权限。

```bash
chmod -R a+rX project
```

这适合递归授予目录可进入权限和文件可读权限，同时避免把所有普通文件都变成可执行文件。

递归修改前应确认目标目录，避免意外扩大大量文件权限。

---

## 九、chmod数字表示

数字表示把每类权限换算为数值：

| 权限 | 数值 |
| --- | ---: |
| `r` | 4 |
| `w` | 2 |
| `x` | 1 |

同一组权限相加：

| 权限 | 计算 | 数值 |
| --- | --- | ---: |
| `---` | 0 | 0 |
| `--x` | 1 | 1 |
| `-w-` | 2 | 2 |
| `-wx` | 2+1 | 3 |
| `r--` | 4 | 4 |
| `r-x` | 4+1 | 5 |
| `rw-` | 4+2 | 6 |
| `rwx` | 4+2+1 | 7 |

三位数字依次代表 owner、group、other：

```text
chmod 640 file
      │││
      ││└── other: ---
      │└─── group: r--
      └──── owner: rw-
```

### 常见文件权限

```text
600  rw-------  私有文件
640  rw-r-----  所有者读写，组成员只读
644  rw-r--r--  所有者读写，其他用户只读
```

### 常见目录和脚本权限

```text
700  rwx------  私有目录或私有脚本
750  rwxr-x---  所有者完全访问，组成员读取和进入
755  rwxr-xr-x  常见公共目录和可执行程序权限
```

练习：

```bash
chmod 640 private.txt
chmod 755 demo.sh
chmod 750 project
ls -ld private.txt demo.sh project
```

### 为什么不应直接使用777

`777` 给予所有用户读取、写入和执行权限。它通常掩盖所有权、用户组或路径配置问题，并扩大误修改和恶意修改的范围。

权限应从实际需求推导：

```text
谁需要访问？
需要读取、修改还是执行？
能否通过用户组共享？
父目录是否允许通过？
```

---

## 十、所有者与所属组

### 1. chown修改所有者

语法：

```text
chown 新所有者 文件
```

修改所有者通常需要管理员权限。

创建练习文件：

```bash
touch owner-demo.txt
ls -l owner-demo.txt
```

暂时改为 root 所有：

```bash
sudo chown root owner-demo.txt
ls -l owner-demo.txt
```

恢复给当前用户：

```bash
sudo chown "$USER" owner-demo.txt
```

### 2. 同时修改所有者和组

```bash
sudo chown "$USER":"$(id -gn)" owner-demo.txt
```

格式为：

```text
所有者:所属组
```

### 3. chgrp修改所属组

```bash
chgrp "$(id -gn)" owner-demo.txt
```

普通用户只能把自己拥有的文件改到自己所属的组。

### 4. 递归修改

```text
chown -R 用户:组 目录
```

`-R` 会修改目录中的所有对象。它适合修复明确范围内的项目目录，不应对 `/`、`/usr`、`/etc` 或未经检查的大目录执行。

---

## 十一、新文件权限与umask

程序创建文件时会提出一个初始权限，再由 `umask` 屏蔽其中部分权限。

查看当前 umask：

```bash
umask
```

常见输出：

```text
0022
```

普通文件的常见基础权限是 `666`：

```text
rw-rw-rw-
```

目录的常见基础权限是 `777`：

```text
rwxrwxrwx
```

应用 `022` 后，常见结果为：

```text
文件：666 屏蔽 022 → 644 → rw-r--r--
目录：777 屏蔽 022 → 755 → rwxr-xr-x
```

这里的计算本质是按权限位屏蔽，不是普通十进制减法。

### 临时修改umask

```bash
umask 0077
touch umask-private.txt
mkdir umask-private-dir
ls -ld umask-private.txt umask-private-dir
```

常见结果：

```text
-rw------- umask-private.txt
drwx------ umask-private-dir
```

恢复本终端常见设置：

```bash
umask 0022
```

umask 只影响之后新创建的对象，不会修改已有文件权限。

---

## 十二、sudo与管理员权限

### 1. sudo做什么

`sudo` 根据系统策略，以另一身份执行一条命令，默认目标身份是 root。

```bash
sudo apt update
```

输入的是当前普通用户的密码，不是 root 密码。终端输入密码时不会显示字符。

### 2. 哪些操作通常需要sudo

- 安装或删除系统软件包。
- 修改 `/etc` 中的系统配置。
- 管理系统服务。
- 修改其他用户拥有的文件。
- 管理用户和用户组。
- 访问仅管理员可用的硬件或内核接口。

用户主目录中的普通开发操作不需要 sudo。

### 3. 不要给所有命令机械添加sudo

如果在项目目录中长期使用 sudo 创建文件，这些文件会归 root 所有，普通用户后续可能无法编辑。

出现权限错误时，先判断：

```text
目标本来是否应该由当前用户访问？
文件所有者是否错误？
所属组是否合适？
目录权限是否允许通过？
```

只有操作本身确实属于系统管理时才使用 sudo。

### 4. sudo缓存

成功验证后，sudo 会在一段时间内缓存授权。再次执行 sudo 可能暂时不要求输入密码。

主动清除当前缓存：

```bash
sudo -k
```

### 5. sudo与su

`sudo 命令` 只提升一条命令的权限，范围清晰。`su` 或 root Shell 会让后续多条命令持续拥有高权限，操作风险更大。

日常管理优先使用明确的 `sudo 命令`。

---

## 十三、用户组成员管理

查看用户组是否存在：

```bash
getent group dialout
```

将当前用户加入附加组的常见写法：

```bash
sudo usermod -aG dialout "$USER"
```

参数含义：

| 参数 | 含义 |
| --- | --- |
| `-G` | 设置附加用户组列表 |
| `-a` | append，在原列表上追加 |

`-aG` 应配合使用。只使用 `-G` 可能用新列表替换原有附加组，导致用户失去其他组身份。

组成员关系在登录时装入进程身份。修改后需要退出并重新登录。在 WSL 中可以关闭全部 WSL 终端，然后在 Windows PowerShell 执行：

```powershell
wsl --shutdown
```

重新打开 Ubuntu 后验证：

```bash
groups
id
```

从用户组移除用户：

```bash
sudo gpasswd -d "$USER" dialout
```

只在确认不再需要该组权限时执行。

---

## 十四、串口设备权限

Linux 开发中常见错误：

```text
Permission denied: /dev/ttyUSB0
```

### 1. 查看设备节点

连接并映射设备后，查看：

```bash
ls -l /dev/ttyUSB0
```

典型输出：

```text
crw-rw---- 1 root dialout ... /dev/ttyUSB0
```

这表示：

- 类型 `c`：字符设备。
- 所有者 `root`：root 拥有设备。
- 所属组 `dialout`：该组成员可以按组权限访问。
- 权限 `rw`：所有者和组成员可以读写。
- 其他用户没有权限。

### 2. 检查当前用户组

```bash
groups
```

若输出不包含 `dialout`，可以加入该组：

```bash
sudo usermod -aG dialout "$USER"
```

重新登录后再次检查。

### 3. WSL中的额外条件

用户组只解决 Linux 内部权限。WSL 还需要先把 USB 设备连接到 WSL 环境，设备节点才会出现。若 `/dev/ttyUSB0` 根本不存在，应先检查 USB 映射、设备识别和驱动，而不是修改权限。

### 4. 不用chmod 777临时解决

直接扩大设备节点权限可能在设备重新连接后失效，也会允许无关用户访问设备。正确方法是确认设备所属组，并让需要访问的用户获得对应组身份。

> **图片占位：** WSL 中 `ls -l /dev/ttyUSB0` 与 `groups` 的输出并排展示，标出设备所属组 `dialout` 和当前用户是否属于该组。

---

## 十五、特殊权限位

普通 `rwx` 之外，Linux 还有 setuid、setgid 和 sticky bit。

### 1. setuid

setuid 设置在可执行文件上。程序运行时会获得文件所有者的有效 UID，而不是调用者 UID。

在 `ls -l` 中，它出现在所有者执行位：

```text
-rwsr-xr-x
```

setuid 程序能够跨越普通权限边界，因此必须经过严格设计与审计。普通脚本和个人程序不应随意设置 setuid。

### 2. setgid用于可执行文件

设置在可执行文件上时，程序运行会获得文件所属组的有效 GID。

```text
-rwxr-sr-x
```

### 3. setgid用于目录

设置在目录上时，新创建对象会继承目录的所属组。这适合团队共享目录。

创建练习目录：

```bash
mkdir shared-project
chmod 2775 shared-project
ls -ld shared-project
```

数字最前面的 `2` 表示 setgid。

输出的组执行位位置会显示 `s`：

```text
drwxrwsr-x
```

### 4. sticky bit

sticky bit 常用于多人可写目录。目录中的用户通常只能删除自己拥有的文件、目录所有者拥有的文件，或由特权用户处理。

典型例子是 `/tmp`：

```bash
ls -ld /tmp
```

常见权限：

```text
drwxrwxrwt
```

最后的 `t` 表示 sticky bit。

练习：

```bash
mkdir sticky-demo
chmod 1777 sticky-demo
ls -ld sticky-demo
```

最前面的 `1` 表示 sticky bit。

### 5. 特殊权限数字

| 特殊权限 | 数值 |
| --- | ---: |
| setuid | 4 |
| setgid | 2 |
| sticky | 1 |

因此：

```text
4755  setuid + rwxr-xr-x
2775  setgid + rwxrwxr-x
1777  sticky + rwxrwxrwx
```

---

## 十六、访问控制列表ACL

传统权限只能为一个所有者、一个所属组和其他用户设置权限。ACL（Access Control List）可以为额外用户或用户组单独授权。

查看 ACL：

```bash
getfacl public.txt
```

若命令不存在，可以安装 `acl` 软件包：

```bash
sudo apt update
sudo apt install -y acl
```

为指定用户增加读取权限的格式：

```text
setfacl -m u:用户名:r 文件
```

为指定组增加读写权限的格式：

```text
setfacl -m g:组名:rw 文件
```

移除指定用户 ACL：

```text
setfacl -x u:用户名 文件
```

存在扩展 ACL 时，`ls -l` 的权限后通常出现 `+`：

```text
-rw-r-----+
```

ACL 适合确实需要例外授权的场景。普通项目优先使用清晰的所有者和用户组设计。

---

## 十七、WSL文件权限特点

WSL 中需要区分两类位置：

### Linux文件系统

例如：

```text
/home/student
/etc
/usr
```

这些位置使用标准 Linux 所有权和权限语义。本章权限实验应放在用户主目录中。

### Windows挂载目录

例如：

```text
/mnt/c
/mnt/d
```

这些目录来自 Windows 文件系统，访问行为同时受到 WSL 挂载配置和 Windows 文件权限影响。`chmod`、所有权、大小写和可执行权限的表现可能与 Linux 用户主目录不同。

需要 Linux 工具链、脚本和权限控制的项目，建议保存在：

```text
/home/用户名/projects
```

这样可以获得一致的 Linux 权限语义。

---

## 十八、Permission denied排查流程

遇到权限错误时，应定位哪一层拒绝访问。

```text
确认当前身份
    ↓
检查目标类型、所有者、所属组和权限
    ↓
检查路径中每一级目录的x权限
    ↓
检查用户是否拥有所需附加组
    ↓
检查ACL和挂载状态
    ↓
判断操作是否确实需要sudo
```

### 第1步：确认身份

```bash
whoami
id
groups
```

### 第2步：检查目标

```bash
ls -ld 目标路径
stat 目标路径
```

确认：

- 目标是文件、目录还是设备。
- 所有者是谁。
- 所属组是什么。
- 当前用户命中 owner、group 还是 other。
- 对应权限是否包含所需操作。

### 第3步：检查完整路径

即使目标文件允许读取，父目录缺少 `x` 也无法访问。

```bash
namei -l /完整/目标/路径
```

`namei -l` 会逐级显示路径中的目录权限和所有者，适合定位是哪一级目录阻止通过。

### 第4步：检查ACL

```bash
getfacl 目标路径
```

ACL 中的 mask 还会限制命名用户、命名组和组权限的最终有效范围。

### 第5步：检查挂载属性

只读文件系统无法写入，即使权限位包含 `w`。

```bash
findmnt -T 目标路径
```

查看挂载选项中是否存在 `ro`（read-only）。

### 第6步：选择正确修复方式

| 原因 | 修复方向 |
| --- | --- |
| 所有者错误 | 修正所有者 |
| 所属组错误 | 修正所属组或用户组成员关系 |
| 权限位不足 | 只增加需要的权限 |
| 父目录不能通过 | 修正对应目录的执行权限 |
| ACL限制 | 调整ACL或mask |
| 文件系统只读 | 解决挂载或底层文件系统问题 |
| 系统管理操作 | 对明确命令使用sudo |

不要使用 `chmod 777` 或长期以 root 运行程序绕过定位过程。

---

## 十九、综合实践：配置一个安全项目目录

### 实践目标

建立一个包含私有配置和可执行脚本的项目目录，为每个对象设置符合用途的权限，并验证结果。

### 第1步：创建项目

```bash
cd ~/linux-course/permission
mkdir -p secure-project/{bin,config,data}
printf '#!/usr/bin/env bash\nprintf "sensor service started\\n"\n' > secure-project/bin/start.sh
printf 'device=/dev/ttyUSB0\nbaud=115200\n' > secure-project/config/device.conf
printf 'sample=25.4\n' > secure-project/data/latest.txt
```

### 第2步：设置目录权限

项目根目录只允许当前用户完全访问：

```bash
chmod 700 secure-project
```

子目录同样保持私有：

```bash
chmod 700 secure-project/bin secure-project/config secure-project/data
```

### 第3步：设置文件权限

启动脚本由所有者读取和执行：

```bash
chmod 500 secure-project/bin/start.sh
```

配置文件由所有者读写：

```bash
chmod 600 secure-project/config/device.conf
```

数据文件由所有者读写：

```bash
chmod 600 secure-project/data/latest.txt
```

### 第4步：验证

```bash
ls -ld secure-project secure-project/*
ls -l secure-project/bin secure-project/config secure-project/data
```

运行脚本：

```bash
./secure-project/bin/start.sh
```

查看配置：

```bash
cat secure-project/config/device.conf
```

追加数据：

```bash
printf 'sample=26.1\n' >> secure-project/data/latest.txt
```

### 第5步：检查身份和最终权限

```bash
id
stat secure-project/bin/start.sh
stat secure-project/config/device.conf
```

### 实践问题

1. 为什么脚本需要 `x` 权限，而配置文件不需要？
2. 为什么目录使用 `700` 而不是 `600`？
3. `500` 的脚本能否被当前用户修改？
4. 如果希望同组成员读取配置，应把权限改成多少？
5. 如果父目录缺少 `x`，内部文件权限为 `644` 是否仍能访问？

> **图片占位：** WSL 终端显示 `secure-project` 的目录与文件权限，并成功运行 `start.sh`。

---

## 二十、常见问题

### 修改权限后仍然无法访问

检查路径中的全部父目录：

```bash
namei -l /完整/目标/路径
```

任一级目录缺少执行权限都会阻止通过。

### sudo创建的项目文件无法编辑

先检查所有者：

```bash
ls -l 文件
```

如果本应属于当前用户，可以修正明确的项目范围：

```bash
sudo chown "$USER":"$(id -gn)" 文件
```

目录树需要递归修复时，先确认绝对路径，再对该项目目录使用 `-R`。

### 加入用户组后groups没有变化

现有进程不会自动获得新的附加组。退出全部 WSL 会话，在 Windows PowerShell 执行：

```powershell
wsl --shutdown
```

重新打开 Ubuntu，再使用 `groups` 验证。

### chmod在/mnt/c中表现不同

`/mnt/c` 位于 Windows 文件系统上，权限行为受到 WSL 挂载配置和 Windows 权限共同影响。把权限实验和 Linux 项目移动到 WSL 用户主目录中。

### 文件有写权限却不能删除

删除由父目录权限控制。检查父目录是否允许当前用户写入和通过。

### 文件没有写权限却可以被删除

只要父目录允许删除目录项，文件本身没有写权限也可能被删除。文件写权限控制内容修改，目录写权限控制名称记录。

### chmod +x后仍无法执行

继续检查：

- 文件格式是否可执行。
- 脚本第一行解释器路径是否正确。
- 文件是否带有 Windows CRLF 换行导致解释器名称异常。
- 所在文件系统是否以 `noexec` 方式挂载。
- 父目录是否允许通过。

---

## 本章小结

Linux 使用 UID 和 GID 表示用户与用户组。文件记录所有者、所属组以及 owner、group、other 三组权限。内核根据访问者身份选择其中一组，不会把三组权限累加。

`r`、`w`、`x` 对普通文件分别表示读取、修改和执行；对目录则表示列出名称、修改目录项和穿过目录。`chmod` 修改权限，`chown` 修改所有者，`chgrp` 修改所属组，`umask` 影响新对象的初始权限。

`sudo` 用于执行明确的系统管理命令。设备访问通常通过用户组授权，例如串口常属于 `dialout`。遇到 `Permission denied` 时，应依次检查身份、目标权限、父目录、附加组、ACL 和挂载状态。

---

## 本章检查点

- 能使用 `whoami`、`id` 和 `groups` 查看身份。
- 能解释 UID、GID、主用户组和附加用户组。
- 能读懂 `-rwxr-x---` 的每一部分。
- 能解释文件和目录的 `rwx` 差异。
- 能使用符号表示修改权限。
- 能把 `rw-r-----` 转换为 `640`，也能反向转换。
- 能使用 `chown` 和 `chgrp` 修改所有者与所属组。
- 能根据 `umask` 判断新文件和目录的常见权限。
- 能说明何时需要 sudo，何时应修复项目所有权。
- 能解释 setuid、setgid 和 sticky bit。
- 能通过设备节点所属组判断串口访问条件。
- 能使用 `namei -l` 定位路径中的权限阻断点。
- 能按最小权限原则解决 `Permission denied`。

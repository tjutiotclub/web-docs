# Linux文件系统与路径

Linux 把普通文件、目录、硬件设备和部分内核运行信息组织在同一棵目录树中。本章建立这套文件系统模型，下一章再使用 Shell 命令完成实际操作。

本系列以 **WSL2 的 Ubuntu** 为统一示例环境。示例用户名使用 `student`，实际路径会随用户名和系统配置变化。

## 学习目标

完成本章后，你应能够：

- 理解 Linux 单一目录树的组织方式。
- 区分根目录、用户主目录和当前工作目录。
- 区分绝对路径与相对路径。
- 理解 `/`、`.`、`..` 和 `~` 在路径中的含义。
- 认识普通文件、目录、链接和设备文件。
- 说明 Linux 主要系统目录的用途。
- 理解 inode、文件名与文件数据之间的关系。
- 理解文件系统、存储设备与挂载点之间的关系。
- 理解 WSL 中 Linux 文件系统和 Windows 磁盘的映射关系。

---

## 一、Linux只有一棵目录树

Windows 常使用盘符区分存储位置：

```text
C:\
D:\
E:\
```

Linux 使用一棵从根目录开始的目录树。根目录写作 `/`，它是所有路径的共同起点。

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

硬盘分区、U 盘、网络存储和虚拟文件系统都通过某个目录接入这棵树。用户访问的是统一路径，不需要为每个 Linux 文件系统分配新的盘符。

根目录和用户主目录不是同一个位置：

```text
/                      Linux目录树的根
/home/student          用户student的主目录
```

这两个概念常被初学者混淆。“根目录”描述文件系统层级，“主目录”描述某个用户保存个人文件的位置。

---

## 二、目录树如何表示位置

路径由一组目录名和文件名组成，各级名称使用正斜杠 `/` 分隔。

```text
/home/student/projects/sensor/main.c
```

从左向右读取：

1. 从根目录 `/` 开始。
2. 进入 `home`。
3. 进入用户目录 `student`。
4. 进入 `projects`。
5. 进入项目目录 `sensor`。
6. 找到文件 `main.c`。

可以把路径理解为目标在目录树中的地址。

```text
/
└── home
    └── student
        └── projects
            └── sensor
                └── main.c
```

Linux 路径使用 `/`，Windows 路径通常使用 `\`。二者不能直接互换：

```text
Linux：   /home/student/projects
Windows： C:\Users\student\projects
```

---

## 三、当前工作目录

每个 Shell 进程都维护一个当前工作目录。相对路径从这个位置开始解释。

假设当前工作目录是：

```text
/home/student/projects/sensor
```

那么相对路径：

```text
src/main.c
```

表示的完整位置是：

```text
/home/student/projects/sensor/src/main.c
```

当前工作目录只影响相对路径，不改变绝对路径的含义。

同一个相对路径在不同位置可能指向不同目标：

```text
当前目录：/home/student/project-a
相对路径：src/main.c
最终位置：/home/student/project-a/src/main.c
```

```text
当前目录：/home/student/project-b
相对路径：src/main.c
最终位置：/home/student/project-b/src/main.c
```

这就是文件操作前必须确认当前目录的原因。

---

## 四、绝对路径与相对路径

### 1. 绝对路径

绝对路径以 `/` 开头，从根目录完整描述目标位置。

```text
/home/student/linux-course/shell/data/sensor01.txt
```

无论当前工作目录在哪里，该路径始终指向同一个目标。

绝对路径适合：

- 配置文件中需要明确指定固定位置。
- 日志需要准确记录文件位置。
- 当前工作目录无法确定。
- 跨越多个目录层级。

### 2. 相对路径

相对路径不以 `/` 开头，以当前工作目录作为起点。

假设当前目录为：

```text
/home/student/linux-course/shell
```

相对路径：

```text
data/sensor01.txt
```

对应绝对路径：

```text
/home/student/linux-course/shell/data/sensor01.txt
```

相对路径适合：

- 在同一项目内部引用文件。
- 让项目整体移动后仍保持内部关系。
- 交互操作时减少重复输入。

### 3. 两种路径描述同一目标

假设当前目录为 `/home/student/project`：

```text
绝对路径：/home/student/project/include/sensor.h
相对路径：include/sensor.h
```

两种写法指向同一个文件，只是起点不同。

---

## 五、路径中的特殊符号

### 根目录 `/`

单独出现的 `/` 表示整棵目录树的根。出现在路径中时，它分隔各级名称。

```text
/
/etc
/etc/hosts
```

### 当前目录 `.`

一个点表示当前工作目录。

```text
./program
./data/sensor.txt
```

`./program` 表示当前目录中的 `program`，而不是从系统命令搜索路径中寻找同名程序。

### 上级目录 `..`

两个点表示当前目录的父目录。

假设当前目录是：

```text
/home/student/project/src
```

则：

```text
..              /home/student/project
../include      /home/student/project/include
../../docs      /home/student/docs
```

每出现一个 `..`，就沿目录树向上移动一级。

### 用户主目录 `~`

波浪号由 Shell 展开为当前用户的主目录。

对用户 `student`：

```text
~                       /home/student
~/projects              /home/student/projects
~/projects/demo         /home/student/projects/demo
```

`~` 是 Shell 语法，不是磁盘上真实存在的目录名。

### 特殊符号总结

| 符号 | 含义 | 示例 |
| --- | --- | --- |
| `/` | 根目录或路径分隔符 | `/etc/hosts` |
| `.` | 当前工作目录 | `./program` |
| `..` | 上级目录 | `../include` |
| `~` | 当前用户主目录 | `~/projects` |

---

## 六、文件名规则

### 1. 区分大小写

以下名称代表三个不同文件：

```text
sensor.txt
Sensor.txt
SENSOR.txt
```

路径中的每一级名称都区分大小写。`Projects` 与 `projects` 是不同目录。

### 2. 点开头表示隐藏条目

名称以 `.` 开头的文件和目录通常被视为隐藏条目：

```text
.bashrc
.config
.git
```

“隐藏”是一种命名约定，不是独立文件属性。它们仍然是普通文件或目录。

用户级配置经常保存在主目录中的隐藏条目里。例如 `.bashrc` 保存 Bash 的用户配置，`.config` 保存许多桌面和命令行程序的配置。

### 3. 扩展名不是类型的决定条件

Linux 文件可以没有扩展名：

```text
Makefile
LICENSE
program
```

扩展名用于表达用途和帮助工具识别文件，但内核不会仅凭 `.txt`、`.c` 或 `.sh` 决定内容类型和执行权限。

### 4. 空格与特殊字符

Linux 文件名可以包含空格：

```text
sensor data.txt
```

Shell 使用空格分隔参数，因此操作这类路径时需要引号或转义。为了提高脚本兼容性，工程文件常使用：

- 英文字母
- 数字
- 短横线 `-`
- 下划线 `_`

例如：

```text
sensor-driver
build_output
lesson01
```

### 5. 路径长度与可读性

多层目录能够表达结构，但层级过深会增加操作成本。项目目录应围绕职责组织：

```text
sensor-demo/
├── src/
├── include/
├── docs/
├── tests/
└── build/
```

这种结构比把所有文件放在同一目录中更容易维护。

---

## 七、Linux主要目录

不同发行版的具体内容有所差异，但关键目录的职责基本一致。

| 目录 | 主要用途 | 典型内容 |
| --- | --- | --- |
| `/home` | 普通用户个人目录 | 文档、项目、用户配置 |
| `/root` | root 用户主目录 | root 的个人文件和配置 |
| `/etc` | 系统范围配置 | 网络、服务、用户配置 |
| `/usr` | 用户空间程序和资源 | 命令、库、头文件、共享数据 |
| `/var` | 经常变化的数据 | 日志、缓存、软件包状态 |
| `/tmp` | 临时数据 | 程序运行时临时文件 |
| `/dev` | 设备和特殊数据通道 | 串口、磁盘、空设备 |
| `/proc` | 进程与内核运行信息 | PID 目录、CPU、内存信息 |
| `/sys` | 设备、驱动与内核对象 | 总线、设备类别、驱动关系 |
| `/boot` | 启动相关文件 | 内核、引导配置 |
| `/mnt` | 常用手动或系统挂载位置 | WSL 中的 Windows 磁盘 |
| `/media` | 可移动设备的常用挂载位置 | U 盘、移动硬盘 |
| `/opt` | 附加第三方软件 | 独立安装的软件目录 |

### `/home`与`/root`

普通用户 `student` 的主目录通常是：

```text
/home/student
```

root 用户的主目录是：

```text
/root
```

`/root` 不是根目录 `/`，也不是 `/home` 的子目录。

### `/etc`

`/etc` 保存系统和服务配置。它面向整个系统，而用户个人配置通常放在主目录中的隐藏文件或 `.config` 目录。

### `/usr`

`/usr` 保存大量用户空间资源：

```text
/usr/bin       常用命令
/usr/lib       程序库
/usr/include   开发头文件
/usr/share     与架构无关的共享数据
```

### `/var`

`/var` 保存运行过程中持续变化的数据：

```text
/var/log       系统和服务日志
/var/cache     缓存
/var/lib       服务和软件包的持久状态
```

### `/tmp`

`/tmp` 用于临时数据。系统可能定期清理其中内容，因此它不适合保存长期项目和重要文件。

---

## 八、文件不只有一种类型

Linux 使用统一的文件系统接口表达不同对象。常见类型包括：

| 类型 | 含义 | 例子 |
| --- | --- | --- |
| 普通文件 | 文本、程序、图片或其他数据 | `main.c`、`program` |
| 目录 | 保存名称与文件对象的对应关系 | `/home/student` |
| 符号链接 | 保存另一个目标的路径 | `current -> releases/v2` |
| 字符设备 | 按字节流访问的设备 | 串口、终端、`/dev/null` |
| 块设备 | 按数据块访问的设备 | 磁盘、存储卡 |
| 命名管道 | 进程间传输数据 | FIFO |
| 套接字 | 本机或网络进程通信端点 | Unix domain socket |

目录本身也是一种文件系统对象。它的内容主要是名称与对象之间的映射关系。

“一切皆文件”表达的是接口统一：许多资源可以通过类似打开、读取、写入和关闭的方式访问。它不表示所有对象都把普通数据永久存储在磁盘中。

---

## 九、inode、文件名与文件数据

理解 inode 可以解释硬链接、删除和文件名之间的关系。

在典型 Linux 文件系统中：

- 目录记录文件名与 inode 的对应关系。
- inode 保存文件类型、权限、所有者、大小、时间等元数据，并关联数据位置。
- 文件名属于目录记录，不直接等于文件数据。

```text
目录项
sensor.txt ──> inode 1052 ──> 文件数据
```

同一个 inode 可以拥有多个文件名：

```text
sensor.txt ──┐
             ├──> inode 1052 ──> 文件数据
backup.txt ──┘
```

这两个名称称为硬链接。删除其中一个名称不会立即删除数据，只要仍有其他硬链接引用该 inode，文件内容仍然存在。

当最后一个硬链接被删除，并且没有进程继续打开该文件时，文件系统才会回收相应数据空间。

---

## 十、符号链接与硬链接

### 1. 符号链接

符号链接保存目标路径：

```text
current -> releases/version-2
```

访问 `current` 时，系统继续解析其保存的目标路径。

符号链接可以：

- 指向普通文件或目录。
- 使用相对路径或绝对路径作为目标。
- 跨越不同文件系统。
- 在目标不存在时继续保留，但会成为失效链接。

常见用途包括：

- 为版本目录提供稳定入口。
- 为较长路径建立短名称。
- 在不复制数据的情况下从另一位置引用目标。

### 2. 硬链接

硬链接是同一 inode 的另一个文件名。它不保存目标路径，而是直接关联同一文件对象。

硬链接的特点：

- 不能跨文件系统。
- 普通用户通常不为目录创建硬链接。
- 删除其中一个名称不影响其他硬链接访问数据。
- 读取任何一个名称都会得到同一份内容。

### 3. 两类链接对比

| 特性 | 符号链接 | 硬链接 |
| --- | --- | --- |
| 本质 | 保存目标路径 | 同一 inode 的另一个名称 |
| 可指向目录 | 可以 | 普通用户通常不可以 |
| 可跨文件系统 | 可以 | 不可以 |
| 原名称删除后 | 可能失效 | 仍可访问数据 |
| 是否拥有独立inode | 是 | 与目标相同 |

工程中最常见的是符号链接，inode 和硬链接则帮助理解文件系统的内部关系。

---

## 十一、`/dev`：把设备放入目录树

`/dev` 中的条目表示设备或特殊数据通道。

常见名称包括：

```text
/dev/null
/dev/zero
/dev/random
/dev/ttyS0
/dev/ttyUSB0
/dev/ttyACM0
/dev/i2c-0
/dev/spidev0.0
```

其中：

- `/dev/null` 丢弃写入的数据。
- `/dev/zero` 读取时产生零字节。
- `/dev/random` 提供随机数据。
- `/dev/ttyS0` 可能表示片上串口。
- `/dev/ttyUSB0` 可能表示 USB 转串口设备。
- `/dev/ttyACM0` 可能表示 USB CDC 串口设备。
- `/dev/i2c-0` 可能表示 I2C 控制器接口。
- `/dev/spidev0.0` 可能表示用户空间 SPI 接口。

设备节点存在需要三个条件共同满足：

```text
硬件存在
  +
内核识别并加载驱动
  +
系统创建或暴露对应接口
```

因此，接上设备却没有出现预期节点时，问题不一定在应用程序，也可能在硬件连接、内核驱动或系统配置。

---

## 十二、`/proc`与`/sys`：运行中的系统视图

### `/proc`

`/proc` 是内核动态提供的虚拟文件系统，主要表达进程和内核运行信息。

典型内容：

```text
/proc/cpuinfo       CPU信息
/proc/meminfo       内存信息
/proc/cmdline       内核启动参数
/proc/1234          PID为1234的进程信息
```

PID 对应的目录会随着进程启动和退出动态出现、消失。

### `/sys`

`/sys` 也是内核提供的虚拟文件系统，主要按照设备、驱动、总线和类别组织内核对象。

```text
/sys/class
/sys/bus
/sys/devices
/sys/block
```

在嵌入式 Linux 中，GPIO、LED、网络接口、存储设备和电源状态等信息可能通过相应内核子系统出现在 `/sys` 中。

### 与普通磁盘目录的区别

`/proc` 和 `/sys` 中的内容由内核在运行时生成：

- 不等同于磁盘中的普通文件。
- 内容会随系统状态变化。
- 文件大小等元数据不一定具有普通文件的含义。
- 部分接口可写，写入行为可能直接改变内核或设备状态。

---

## 十三、文件系统与挂载

### 1. 文件系统是什么

文件系统规定数据如何在存储介质上组织、命名和记录。常见类型包括：

| 文件系统 | 常见场景 |
| --- | --- |
| ext4 | Linux桌面、服务器、开发板根文件系统 |
| XFS | 大容量Linux服务器 |
| Btrfs | 支持快照和高级存储管理的Linux系统 |
| NTFS | Windows磁盘 |
| FAT32 | U盘、存储卡和跨平台交换 |
| tmpfs | 使用内存保存的临时文件系统 |
| proc | 提供进程与内核运行信息 |
| sysfs | 提供设备与内核对象信息 |

### 2. 存储设备、分区与文件系统

三者处于不同层次：

```text
存储设备
  ↓ 划分
分区
  ↓ 格式化
文件系统
  ↓ 挂载
Linux目录树中的目录
```

一个磁盘可以包含多个分区，每个分区可以拥有不同文件系统。

### 3. 挂载点

挂载把一个文件系统接入现有目录树。接入位置称为挂载点。

```text
Linux目录树
/
└── mnt
    └── data  ← 另一个文件系统的挂载点
```

挂载完成后，访问 `/mnt/data` 就是在访问该文件系统的根。

同一个目录树可以同时组合：

- Linux 根文件系统
- Windows 磁盘
- 内存文件系统
- 内核虚拟文件系统
- 网络文件系统
- 外接存储设备

这解释了为什么 Linux 不需要为每个存储设备建立新的盘符。

### 4. 卸载的含义

卸载会解除文件系统与挂载点的连接。它不等于删除文件系统中的数据。

设备仍在被程序使用时，系统通常会拒绝卸载，以防正在访问的数据失去连接。

---

## 十四、WSL中的文件系统关系

WSL2 同时连接 Linux 文件系统和 Windows 文件系统。

### 1. Linux用户主目录

WSL 用户 `student` 的主目录通常是：

```text
/home/student
```

Linux 项目、编译目录和需要 Linux 权限语义的文件适合保存在这里。

Windows 可以通过网络样式路径访问该目录：

```text
\\wsl$\Ubuntu\home\student
```

这里的 `Ubuntu` 是 WSL 发行版名称。

### 2. Windows磁盘

WSL 通常把 Windows 盘符挂载到 `/mnt`：

```text
Windows C:\      ↔ WSL /mnt/c
Windows D:\      ↔ WSL /mnt/d
```

例如：

```text
Windows：C:\Users\Public\Documents
WSL：    /mnt/c/Users/Public/Documents
```

> **图片占位：** 一张路径映射示意图，展示 Windows 的 `C:\Users\Public`、WSL 的 `/mnt/c/Users/Public` 和 WSL 主目录 `\\wsl$\Ubuntu\home\用户名` 之间的关系。

### 3. 项目位置选择

需要由 Linux 编译器、包管理器、脚本和权限系统频繁操作的项目，放在：

```text
/home/用户名/projects
```

需要由 Windows 软件直接管理的大型普通文件，可以放在：

```text
/mnt/c
/mnt/d
```

一个项目应尽量固定在同一种文件系统环境中，减少路径格式、权限、大小写、换行符和文件系统性能差异带来的问题。

---

## 十五、从文件路径理解工程结构

考虑一个嵌入式应用项目：

```text
sensor-app/
├── src/
│   ├── main.c
│   └── sensor.c
├── include/
│   └── sensor.h
├── config/
│   └── app.conf
├── tests/
│   └── test_sensor.c
├── docs/
│   └── protocol.md
└── build/
```

每个目录承担清晰职责：

| 目录 | 职责 |
| --- | --- |
| `src` | 程序实现 |
| `include` | 对外头文件 |
| `config` | 运行配置 |
| `tests` | 测试代码 |
| `docs` | 项目文档 |
| `build` | 构建产物 |

假设当前目录为 `sensor-app/src`：

```text
main.c                  当前目录中的源文件
../include/sensor.h     上级目录中的头文件
../config/app.conf      上级目录中的配置文件
../build                上级目录中的构建目录
```

这种路径关系不会依赖项目位于 `/home/student/projects` 还是其他位置，因此项目内部常使用相对关系组织构建和配置。

---

## 十六、概念练习

### 练习一：还原绝对路径

已知当前目录：

```text
/home/student/project/src/module
```

写出下列相对路径对应的绝对位置：

```text
main.c
../sensor.c
../../include/sensor.h
../../../docs/readme.md
```

参考结果：

```text
/home/student/project/src/module/main.c
/home/student/project/src/sensor.c
/home/student/project/include/sensor.h
/home/student/docs/readme.md
```

### 练习二：写出相对路径

已知当前目录：

```text
/home/student/project/src
```

目标文件：

```text
/home/student/project/docs/protocol.md
```

对应相对路径：

```text
../docs/protocol.md
```

### 练习三：判断文件系统对象

判断以下对象最可能属于哪种类型：

| 路径 | 类型 |
| --- | --- |
| `/home/student/main.c` | 普通文件 |
| `/home/student/projects` | 目录 |
| `/dev/ttyUSB0` | 字符设备 |
| `/proc/cpuinfo` | proc虚拟文件 |
| `current -> releases/v2` | 符号链接 |
| `/dev/sda` | 块设备 |

### 练习四：分析WSL路径

将下列 Windows 路径写成 WSL 中的对应位置：

```text
C:\Users\Public\Downloads
D:\datasets\sensor
```

参考结果：

```text
/mnt/c/Users/Public/Downloads
/mnt/d/datasets/sensor
```

---

## 十七、常见概念误区

### 根目录就是root用户主目录

二者位置不同：

```text
/          根目录
/root      root用户主目录
```

### 文件扩展名决定文件能否执行

Linux 是否允许执行文件主要取决于权限、文件格式和解释器。扩展名只表达用途。

### 文件名和文件数据是一回事

文件名属于目录项，它关联 inode；inode 再关联文件元数据和数据。硬链接正是多个名称关联同一 inode。

### `/proc`中的内容都保存在磁盘上

`/proc` 的内容由内核动态生成，反映当前运行状态。

### Windows路径可以直接粘贴到Linux命令中

Windows 与 Linux 使用不同路径表示。WSL 中应把盘符转换为 `/mnt/盘符小写`，并把 `\` 转为 `/`。

### 删除符号链接等于删除目标

符号链接和目标是两个文件系统对象。删除链接通常只删除链接本身，不会删除目标；通过链接访问后主动修改目标内容则会影响目标。

---

## 本章小结

Linux 使用从 `/` 开始的单一目录树。绝对路径从根目录开始，相对路径从当前工作目录开始；`.`、`..` 和 `~` 分别表达当前目录、上级目录和用户主目录。

普通文件、目录、符号链接、设备节点和虚拟文件系统都进入同一命名空间。`/home` 保存用户文件，`/etc` 保存系统配置，`/usr` 保存程序与开发资源，`/var` 保存变化数据；`/dev`、`/proc` 和 `/sys` 分别表达设备接口、进程与内核状态、设备与驱动关系。

文件系统通过挂载点接入目录树。WSL 将 Windows 磁盘挂载到 `/mnt/c`、`/mnt/d` 等位置，同时允许 Windows 通过 `\\wsl$` 访问 Linux 用户目录。

下一章将把这些概念转化为实际操作：查看和切换目录、创建文件、复制与移动数据、搜索内容，并使用管道和重定向组合命令。

---

## 本章检查点

- 能解释根目录、主目录和当前工作目录的区别。
- 能为同一文件写出绝对路径和相对路径。
- 能说明 `/`、`.`、`..` 和 `~` 的含义。
- 能解释 Linux 文件名的大小写和隐藏规则。
- 能说明 `/home`、`/etc`、`/usr`、`/var` 和 `/tmp` 的用途。
- 能区分普通文件、目录、链接、字符设备和块设备。
- 能解释文件名、inode 和文件数据之间的关系。
- 能比较符号链接与硬链接。
- 能说明 `/dev`、`/proc` 和 `/sys` 的职责。
- 能解释设备、分区、文件系统和挂载点之间的关系。
- 能写出 Windows 路径在 WSL 中的常见映射形式。

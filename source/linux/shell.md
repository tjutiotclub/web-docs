# Shell命令基础

Shell 将单个命令组合成完整的数据处理流程。本章从命令结构开始，学习文件操作、文本查看、通配符、搜索、管道和重定向，并完成一次日志整理实践。

本章所有示例均在 **WSL2 的 Ubuntu** 中执行。权限、进程管理和 Shell 脚本将在后续章节展开。

## 学习目标

完成本章后，你应能够：

- 读懂命令、选项和参数的关系。
- 判断命令来自 Shell、可执行文件还是别名。
- 安全地创建、复制、移动、重命名和删除文件。
- 使用 `cat`、`less`、`head`、`tail` 和 `wc` 查看文本。
- 使用通配符批量匹配文件。
- 使用 `find` 查找文件，使用 `grep` 搜索内容。
- 理解标准输入、标准输出和标准错误。
- 使用管道与重定向组合命令。
- 使用引号正确处理变量、空格和特殊字符。
- 从 `--help` 和 `man` 中独立查询命令用法。

---

## 一、准备练习环境

打开 WSL Ubuntu 终端，创建本章专用目录：

```bash
mkdir -p ~/linux-course/shell/{data,logs,backup,output}
cd ~/linux-course/shell
pwd
```

典型输出：

```text
/home/student/linux-course/shell
```

花括号会让 Shell 一次生成多个名称，因此上面的 `mkdir` 创建四个子目录。

创建练习文件：

```bash
printf "temperature=25\nhumidity=40\nstatus=ok\n" > data/sensor01.txt
printf "temperature=28\nhumidity=45\nstatus=ok\n" > data/sensor02.txt
printf "temperature=31\nhumidity=52\nstatus=warning\n" > data/sensor03.txt
printf "2026-09-28 10:00:01 INFO system started\n2026-09-28 10:00:05 INFO sensor ready\n2026-09-28 10:01:10 WARN temperature high\n2026-09-28 10:01:12 ERROR sensor timeout\n2026-09-28 10:01:15 INFO retry success\n" > logs/system.log
```

确认目录和文件：

```bash
find . -maxdepth 2 -print
```

输出应包含：

```text
.
./data
./data/sensor01.txt
./data/sensor02.txt
./data/sensor03.txt
./logs
./logs/system.log
./backup
./output
```

本章涉及覆盖与删除的示例只操作 `~/linux-course/shell` 中的练习文件。

> **图片占位：** WSL 终端中创建练习目录与文件，并显示 `find . -maxdepth 2 -print` 的结果。

---

## 二、Shell如何执行一条命令

一条常见命令由命令名、选项和参数组成：

```text
命令 [选项] [参数]
```

例如：

```bash
ls -l data
```

其中：

| 部分 | 内容 | 作用 |
| --- | --- | --- |
| 命令 | `ls` | 启动列出目录内容的功能 |
| 选项 | `-l` | 使用详细格式显示 |
| 参数 | `data` | 指定操作对象 |

方括号在帮助文档中表示该部分可选，实际输入时不写方括号。

### 1. 短选项

短选项通常由一个短横线和一个字母组成：

```bash
ls -l
ls -a
ls -h
```

部分短选项可以合并：

```bash
ls -lah
```

它等价于：

```bash
ls -l -a -h
```

### 2. 长选项

长选项通常以两个短横线开头：

```bash
ls --all
ls --human-readable
```

长选项更容易阅读，短选项更适合频繁输入。

### 3. 带值的选项

有些选项还需要一个值：

```bash
head -n 3 logs/system.log
```

`-n 3` 表示只显示前三行。

### 4. 参数可以有多个

```bash
ls data logs output
```

该命令依次列出三个目录的内容。

### 5. 使用`--`结束选项解析

文件名以 `-` 开头时，命令可能把它误认为选项。创建练习文件：

```bash
touch -- -report.txt
```

查看该文件：

```bash
ls -l -- -report.txt
```

`--` 告诉命令：后面的内容全部按参数处理，不再解释为选项。

删除练习文件：

```bash
rm -- -report.txt
```

---

## 三、命令来自哪里

Shell 接收到命令名后，需要确定应该执行什么。命令可能是 Shell 内建命令、外部可执行文件、别名或函数。

### 使用type判断命令类型

```bash
type cd
type ls
type grep
```

可能看到：

```text
cd is a shell builtin
ls is aliased to `ls --color=auto'
grep is /usr/bin/grep
```

- `cd` 是 Shell 内建命令，因为改变当前目录必须由当前 Shell 自己完成。
- `ls` 可能被配置为别名。
- `grep` 通常是 `/usr/bin` 中的外部程序。

### 使用command -v查找命令

```bash
command -v gcc
command -v python3
```

如果命令存在，会输出对应路径或命令定义；不存在时不会输出成功结果。

### 使用which查找可执行文件

```bash
which gcc
```

`which` 常用于查找 `PATH` 中的外部可执行文件。判断别名和内建命令时，`type` 或 `command -v` 更完整。

### PATH环境变量

```bash
echo "$PATH"
```

`PATH` 保存一组以冒号分隔的目录。输入命令名时，Shell 会按顺序在这些目录中寻找可执行文件。

当前目录通常不在 `PATH` 中。因此，执行当前目录中的程序时需要写：

```text
./program
```

这明确告诉 Shell 从当前目录寻找 `program`。

---

## 四、Shell的解析顺序

按下 Enter 后，Shell 会先处理输入，再启动命令。初学阶段需要认识以下步骤：

```text
读取输入
  ↓
处理引号和转义
  ↓
展开变量、波浪号和通配符
  ↓
处理重定向和管道
  ↓
查找并执行命令
```

例如：

```bash
ls "$HOME"/linux-course/shell/data/*.txt
```

执行前发生了两次展开：

1. `$HOME` 展开为用户主目录。
2. `*.txt` 展开为目录中匹配的文本文件名。

最终 `ls` 接收到的是多个明确路径。

理解“Shell 先展开，命令后执行”，可以解释通配符、变量和引号的许多行为。

---

## 五、路径与目录导航

上一章建立了目录树和路径模型。本节使用 `pwd`、`cd` 和 `ls` 在 WSL 文件系统中实际观察和切换位置。

### 1. pwd：确认当前工作目录

```bash
pwd
```

`pwd` 输出当前工作目录的绝对路径。在执行相对路径操作前，应先用它确认起点。

### 2. cd：切换目录

回到用户主目录：

```bash
cd ~
```

不带参数的写法效果相同：

```bash
cd
```

进入本章目录：

```bash
cd ~/linux-course/shell
```

进入上级目录：

```bash
cd ..
```

进入绝对路径：

```bash
cd /tmp
```

返回上一次工作目录：

```bash
cd -
```

`cd -` 适合在两个目录之间切换。

### 3. ls：列出目录内容

列出当前目录：

```bash
cd ~/linux-course/shell
ls
```

列出指定目录：

```bash
ls data
```

详细显示：

```bash
ls -l data
```

显示隐藏条目：

```bash
ls -la data
```

使用易读单位显示大小：

```bash
ls -lh logs/system.log
```

只查看目录本身，而不是列出其中内容：

```bash
ls -ld data
```

### 4. Tab补全路径

输入：

```text
cd ~/linux-course/sh
```

按 Tab，Shell 会尝试补全为：

```bash
cd ~/linux-course/shell/
```

只有一个匹配项时直接补全；存在多个候选项时，连续按两次 Tab 查看候选。

### 5. 处理含空格的路径

```bash
mkdir -p "output/test data"
cd "output/test data"
pwd
```

也可以转义空格：

```bash
cd ~/linux-course/shell
cd output/test\ data
```

完成后回到本章目录：

```bash
cd ~/linux-course/shell
```

### 6. 导航练习

从 `~/linux-course/shell` 出发，完成：

```bash
cd data
pwd
ls -la
cd ../logs
pwd
ls -lh
cd -
pwd
```

观察 `..` 和 `cd -` 的区别：`..` 根据目录树返回父目录，`cd -` 返回上一次工作目录。

---

## 六、文件与目录操作

### 1. mkdir：创建目录

创建单个目录：

```bash
mkdir reports
```

创建多层目录：

```bash
mkdir -p reports/2026/september
```

`-p` 会创建不存在的父目录；目标已经存在时也不会因此报错。

### 2. touch：创建空文件或更新时间

```bash
touch reports/summary.txt
ls -l reports/summary.txt
```

再次执行 `touch` 不会清空文件，只会更新访问时间和修改时间。

### 3. cp：复制文件

复制一个文件：

```bash
cp data/sensor01.txt backup/sensor01.txt
```

源文件保持不变，目标位置出现一份独立副本。

复制到目录并保留原名：

```bash
cp data/sensor02.txt backup/
```

一次复制多个文件到目录：

```bash
cp data/sensor01.txt data/sensor02.txt backup/
```

目标是目录时，目标目录必须写在最后。

### 4. cp -r：复制目录

```bash
cp -r data backup/data-copy
```

`-r` 表示递归复制目录及其中内容。

查看结果：

```bash
find backup -maxdepth 2 -print
```

### 5. cp -i：覆盖前确认

```bash
cp -i data/sensor01.txt backup/sensor01.txt
```

目标文件已经存在时，`-i` 会询问是否覆盖：

```text
cp: overwrite 'backup/sensor01.txt'?
```

输入 `y` 并按 Enter 执行覆盖，输入 `n` 放弃。

### 6. mv：移动和重命名

重命名文件：

```bash
mv reports/summary.txt reports/monthly-summary.txt
```

移动文件到其他目录：

```bash
mv reports/monthly-summary.txt output/
```

`mv` 的源和目标位于同一文件系统时，通常只需更新目录记录，不会重新复制全部内容。

覆盖前确认：

```bash
mv -i 源文件 目标文件
```

### 7. rm：删除文件

先创建专用测试文件：

```bash
touch output/delete-me.txt
```

确认目标：

```bash
ls -l output/delete-me.txt
```

交互式删除：

```bash
rm -i output/delete-me.txt
```

输入 `y` 后删除文件。

命令行中的 `rm` 通常不会把文件移入 Windows 回收站。删除前应确认当前目录、目标路径和通配符展开结果。

### 8. rmdir：删除空目录

```bash
mkdir output/empty-dir
rmdir output/empty-dir
```

`rmdir` 只能删除空目录，因此适合需要避免误删目录内容的场景。

### 9. rm -r：递归删除目录

递归删除会连同目录内容一起删除。先创建一个明确的练习目标：

```bash
mkdir -p output/remove-test/subdir
touch output/remove-test/subdir/file.txt
find output/remove-test -print
```

确认目标后执行：

```bash
rm -r output/remove-test
```

实际工程中，应先使用 `pwd`、`ls` 或 `find` 检查目标，再执行递归删除。不要把未检查的变量、通配符或根目录交给递归删除命令。

---

## 七、查看文件类型与链接

### 1. file：判断内容类型

```bash
file data/sensor01.txt
file /usr/bin/ls
```

`file` 根据内容和文件结构判断类型，不只依赖扩展名。

### 2. stat：查看元数据

```bash
stat data/sensor01.txt
```

输出包含文件大小、inode、权限、所有者和时间信息。

只输出 inode 编号：

```bash
stat -c '%i %n' data/sensor01.txt
```

### 3. ln -s：创建符号链接

```bash
ln -s data/sensor01.txt sensor-current
ls -l sensor-current
cat sensor-current
```

符号链接保存目标路径。查看链接中记录的目标：

```bash
readlink sensor-current
```

解析为最终绝对路径：

```bash
readlink -f sensor-current
```

### 4. ln：创建硬链接

```bash
ln data/sensor01.txt sensor-hard
ls -li data/sensor01.txt sensor-hard
```

两个名称显示相同 inode，说明它们引用同一文件对象。

本章练习结束后可以删除链接名称：

```bash
rm sensor-current sensor-hard
```

原文件 `data/sensor01.txt` 不受影响。

---

## 八、观察文件系统与WSL路径

### 1. findmnt：查看挂载关系

```bash
findmnt
```

只查看某个路径所在的挂载关系：

```bash
findmnt -T ~
findmnt -T /mnt/c
```

### 2. df：查看文件系统空间

```bash
df -h ~
df -h /mnt/c
```

`-h` 使用易读单位显示总容量、已用空间和可用空间。

### 3. lsblk：查看块设备

```bash
lsblk
```

WSL2 使用虚拟磁盘，因此输出与物理 Linux 主机不同，但列出的设备、大小和挂载信息采用相同表达方式。

### 4. 在WSL中访问Windows磁盘

```bash
ls /mnt/c
ls /mnt/c/Users
```

C 盘映射为 `/mnt/c`，其他盘符通常采用相同规则。

### 5. 转换路径格式

Windows路径转换为WSL路径：

```bash
wslpath 'C:\Users\Public'
```

WSL路径转换为Windows路径：

```bash
wslpath -w ~/linux-course/shell
```

### 6. 从WSL打开Windows文件资源管理器

```bash
cd ~/linux-course/shell
explorer.exe .
```

末尾的 `.` 表示当前目录。

---

## 九、查看文本内容

### 1. cat：一次输出完整内容

```bash
cat data/sensor01.txt
```

输出：

```text
temperature=25
humidity=40
status=ok
```

同时查看多个文件：

```bash
cat data/sensor01.txt data/sensor02.txt
```

`cat` 适合短文本。大文件会快速刷过终端，应使用 `less` 分页查看。

显示行号：

```bash
cat -n logs/system.log
```

### 2. less：分页查看

```bash
less logs/system.log
```

常用按键：

| 按键 | 作用 |
| --- | --- |
| `↑`、`↓` | 上下移动一行 |
| `PageUp`、`PageDown` | 上下翻页 |
| `/关键词` | 向后搜索 |
| `n` | 跳到下一个匹配项 |
| `N` | 跳到上一个匹配项 |
| `g` | 跳到文件开头 |
| `G` | 跳到文件末尾 |
| `q` | 退出 |

`less` 不会修改文件内容。

### 3. head：查看开头

默认显示前十行：

```bash
head logs/system.log
```

显示前三行：

```bash
head -n 3 logs/system.log
```

也可以简写：

```bash
head -3 logs/system.log
```

### 4. tail：查看结尾

默认显示最后十行：

```bash
tail logs/system.log
```

显示最后两行：

```bash
tail -n 2 logs/system.log
```

### 5. tail -f：持续观察日志

```bash
tail -f logs/system.log
```

`-f` 表示 follow。文件末尾出现新内容时，`tail` 会持续输出，适合观察运行中的程序日志。

该命令不会主动结束。按：

```text
Ctrl + C
```

停止观察并返回提示符。

### 6. wc：统计行、单词和字节

```bash
wc logs/system.log
```

分别只统计行数、单词数和字节数：

```bash
wc -l logs/system.log
wc -w logs/system.log
wc -c logs/system.log
```

统计日志行数时最常使用：

```bash
wc -l logs/system.log
```

---

## 十、通配符与批量匹配

通配符由 Shell 展开，用于一次匹配多个路径。

回到练习目录：

```bash
cd ~/linux-course/shell
```

### 1. `*`匹配任意长度字符

```bash
ls data/*.txt
```

匹配 `data` 中所有以 `.txt` 结尾的名称。

```bash
ls data/sensor*
```

匹配所有以 `sensor` 开头的名称。

`*` 也可以匹配零个字符。

### 2. `?`匹配一个字符

```bash
ls data/sensor0?.txt
```

`?` 只能匹配一个字符，因此可以匹配 `sensor01.txt`、`sensor02.txt` 和 `sensor03.txt`。

### 3. `[]`匹配字符集合

```bash
ls data/sensor0[12].txt
```

只匹配编号末位为 `1` 或 `2` 的文件。

范围写法：

```bash
ls data/sensor0[1-3].txt
```

### 4. 通配符不会默认匹配隐藏文件

```bash
touch data/.hidden.txt
printf '%s\n' data/*
```

结果通常不包含 `.hidden.txt`。查看隐藏文件需要显式使用：

```bash
ls -la data
```

### 5. 先预览再批量操作

复制所有传感器文本前，先查看展开结果：

```bash
printf '%s\n' data/sensor*.txt
```

确认后再执行：

```bash
cp data/sensor*.txt backup/
```

这种“先打印、后操作”的习惯对移动和删除命令尤其重要。

### 6. 花括号展开

花括号不是文件匹配，而是生成字符串组合：

```bash
printf '%s\n' sensor{01,02,03}.txt
```

输出：

```text
sensor01.txt
sensor02.txt
sensor03.txt
```

生成连续编号：

```bash
printf '%s\n' sample{1..5}.dat
```

花括号展开不检查文件是否存在。

---

## 十一、使用find查找文件

`find` 从指定目录开始递归查找路径。

基本结构：

```text
find 起始目录 查找条件
```

### 1. 按名称查找

```bash
find . -name 'sensor01.txt'
```

文件名模式应放在引号中，让 `find` 处理 `*`，避免 Shell 提前展开。

查找所有文本文件：

```bash
find . -name '*.txt'
```

### 2. 忽略大小写

```bash
find . -iname '*.TXT'
```

`-iname` 忽略名称大小写。

### 3. 按类型查找

只查找普通文件：

```bash
find . -type f
```

只查找目录：

```bash
find . -type d
```

只查找符号链接：

```bash
find . -type l
```

### 4. 限制搜索深度

```bash
find . -maxdepth 2 -type f
```

`-maxdepth 2` 表示最多向下搜索两层。

### 5. 组合条件

查找 `data` 中名称以 `sensor` 开头的普通文本文件：

```bash
find data -type f -name 'sensor*.txt'
```

### 6. 使用-print0安全传递复杂文件名

普通换行分隔无法可靠表示包含换行符的文件名。工程脚本需要把 `find` 结果交给其他命令时，可以使用空字符分隔：

```bash
find data -type f -print0
```

对应的接收命令必须支持空字符输入，例如 `xargs -0`。初学阶段先记住：路径可以包含空格，脚本不能随意按空格拆分文件名。

---

## 十二、使用grep搜索文本

`grep` 按行搜索文本，并输出匹配行。

基本结构：

```text
grep [选项] 搜索模式 文件
```

### 1. 基本搜索

```bash
grep WARN logs/system.log
```

输出：

```text
2026-09-28 10:01:10 WARN temperature high
```

### 2. 显示行号

```bash
grep -n ERROR logs/system.log
```

输出开头会包含匹配行号。

### 3. 忽略大小写

```bash
grep -i error logs/system.log
```

可以同时匹配 `ERROR`、`Error` 和 `error`。

### 4. 反向匹配

```bash
grep -v INFO logs/system.log
```

输出不包含 `INFO` 的行。

### 5. 统计匹配行数

```bash
grep -c INFO logs/system.log
```

`-c` 输出匹配行的数量。

### 6. 搜索多个文件

```bash
grep status data/*.txt
```

多个文件参与搜索时，输出会在匹配行前显示文件名。

### 7. 递归搜索目录

```bash
grep -R -n warning data
```

`-R` 递归读取目录，`-n` 显示行号。

### 8. 使用扩展正则表达式

查找 WARN 或 ERROR：

```bash
grep -E 'WARN|ERROR' logs/system.log
```

`-E` 启用扩展正则表达式，`|` 表示“或者”。

### 9. 按普通字符串搜索

搜索内容包含正则特殊字符时，可以使用固定字符串模式：

```bash
grep -F 'temperature=31' data/sensor03.txt
```

`-F` 将模式作为普通字符串处理。

---

## 十三、标准输入、标准输出与标准错误

Linux 程序启动时通常拥有三个标准数据通道：

| 名称 | 文件描述符 | 默认连接 |
| --- | ---: | --- |
| 标准输入 stdin | 0 | 键盘 |
| 标准输出 stdout | 1 | 终端 |
| 标准错误 stderr | 2 | 终端 |

```text
键盘 ──标准输入──> 程序
                     ├──标准输出──> 终端
                     └──标准错误──> 终端
```

标准输出用于正常结果，标准错误用于诊断信息。两者默认都显示在终端，所以视觉上可能很难区分；重定向后可以分别处理。

### 观察标准输出

```bash
printf "normal output\n"
```

### 观察标准错误

访问不存在的文件：

```bash
ls missing-file.txt
```

错误信息通过标准错误输出。

---

## 十四、输出重定向

重定向由 Shell 处理，它会在启动命令前连接输入输出目标。

### 1. `>`覆盖标准输出

```bash
grep INFO logs/system.log > output/info.log
```

终端不再显示匹配内容，结果写入文件。查看：

```bash
cat output/info.log
```

再次使用 `>` 会先清空原文件，再写入新结果：

```bash
grep WARN logs/system.log > output/info.log
```

现在 `info.log` 只包含 WARN 行。

### 2. `>>`追加标准输出

```bash
grep ERROR logs/system.log >> output/info.log
```

`>>` 把内容追加到文件末尾，不清除已有内容。

### 3. `2>`重定向标准错误

```bash
ls data missing-dir > output/list.txt 2> output/error.log
```

正常输出进入 `list.txt`，错误信息进入 `error.log`。

查看：

```bash
cat output/list.txt
cat output/error.log
```

### 4. `2>>`追加标准错误

```bash
ls another-missing-file 2>> output/error.log
```

### 5. 合并标准输出和标准错误

```bash
ls data missing-dir > output/all.log 2>&1
```

`2>&1` 表示让文件描述符 2 指向文件描述符 1 当前的目标，因此正常输出和错误信息都进入 `all.log`。

Bash 也支持简写：

```bash
ls data missing-dir &> output/all.log
```

### 6. 丢弃不需要的输出

```bash
command -v gcc > /dev/null
```

`/dev/null` 会丢弃写入的数据。

同时丢弃标准输出和标准错误：

```bash
ls missing-file > /dev/null 2>&1
```

调试阶段不应随意丢弃错误信息，否则会失去定位依据。

---

## 十五、输入重定向

`<` 将文件连接到程序的标准输入：

```bash
wc -l < logs/system.log
```

输出只有数字：

```text
5
```

对比：

```bash
wc -l logs/system.log
```

后者由 `wc` 自己打开文件，因此输出通常同时包含行数和文件名。

许多命令既能从文件参数读取，也能从标准输入读取。标准输入让它们能够参与管道。

---

## 十六、使用管道组合命令

管道符 `|` 把左侧命令的标准输出连接到右侧命令的标准输入：

```text
命令1的标准输出 | 命令2的标准输入
```

### 1. 统计匹配行

```bash
grep INFO logs/system.log | wc -l
```

执行过程：

```text
grep筛选INFO行 → wc统计行数
```

### 2. 分页查看长输出

```bash
find /usr/bin -maxdepth 1 -type f | less
```

`find` 产生大量路径，`less` 分页显示。

### 3. 多级管道

```bash
grep -E 'WARN|ERROR' logs/system.log | sort | wc -l
```

数据依次经过搜索、排序和统计。

### 4. 管道只传递标准输出

```bash
ls data missing-dir | wc -l
```

`data` 的正常结果进入 `wc`，`missing-dir` 的错误仍直接显示在终端，因为标准错误默认不进入管道。

若确实需要把错误也交给右侧命令，可以先合并：

```bash
ls data missing-dir 2>&1 | wc -l
```

### 5. 每个命令只完成一个任务

管道的价值来自组合：

```text
产生数据 → 筛选 → 转换 → 排序 → 统计 → 保存
```

这种结构比一个承担所有工作的巨大命令更容易测试和复用。

---

## 十七、tee：显示并保存输出

普通 `>` 重定向后，结果不会同时显示在终端。`tee` 从标准输入读取数据，一份写入文件，一份继续输出。

```bash
grep -E 'WARN|ERROR' logs/system.log | tee output/alerts.log
```

终端会显示结果，同时生成 `output/alerts.log`。

追加写入：

```bash
grep INFO logs/system.log | tee -a output/alerts.log
```

`tee` 常用于保存构建日志：

```text
构建命令 2>&1 | tee build.log
```

这样既能实时观察，也能保留完整记录。

---

## 十八、常用文本处理命令

### 1. sort：排序

```bash
printf "sensor03\nsensor01\nsensor02\n" | sort
```

输出：

```text
sensor01
sensor02
sensor03
```

数字排序使用：

```bash
printf "10\n2\n30\n" | sort -n
```

### 2. uniq：处理相邻重复行

```bash
printf "ok\nok\nwarning\nwarning\n" | uniq
```

`uniq` 只合并相邻重复行，因此处理无序数据时通常先排序：

```bash
printf "ok\nwarning\nok\nwarning\n" | sort | uniq
```

统计每种值的数量：

```bash
printf "ok\nwarning\nok\nwarning\n" | sort | uniq -c
```

### 3. cut：按分隔符提取字段

传感器文件使用 `=` 分隔键和值：

```bash
cut -d '=' -f 1 data/sensor01.txt
```

- `-d '='` 指定分隔符。
- `-f 1` 提取第一个字段。

提取值：

```bash
cut -d '=' -f 2 data/sensor01.txt
```

### 4. tr：字符转换

```bash
printf "warning\n" | tr 'a-z' 'A-Z'
```

输出：

```text
WARNING
```

删除回车字符的常见写法：

```bash
tr -d '\r' < windows-text.txt > linux-text.txt
```

### 5. xargs：把标准输入转换为参数

```bash
printf "data/sensor01.txt\ndata/sensor02.txt\n" | xargs wc -l
```

`xargs` 将输入中的路径作为 `wc -l` 的命令参数。

处理文件名时，推荐使用空字符分隔：

```bash
find data -type f -name '*.txt' -print0 | xargs -0 wc -l
```

这样可以正确处理包含空格的文件名。

---

## 十九、引号与转义

引号控制 Shell 如何解释空格、变量和特殊字符。

### 1. 不加引号

```bash
echo $HOME
```

变量会展开，展开结果还可能继续参与单词拆分和通配符匹配。

变量作为路径或文本参数时，通常应使用双引号：

```bash
echo "$HOME"
```

### 2. 单引号

单引号中的内容按字面值处理：

```bash
echo '$HOME'
```

输出：

```text
$HOME
```

单引号适合正则表达式、通配模式和不需要变量展开的固定文本。

### 3. 双引号

双引号保留空格，同时允许变量和命令替换：

```bash
echo "home directory: $HOME"
```

### 4. 反斜杠转义

反斜杠让后面的单个字符失去特殊含义：

```bash
echo \$HOME
```

输出：

```text
$HOME
```

处理空格路径：

```bash
mkdir test\ data
cd test\ data
```

### 5. 路径变量必须加双引号

```bash
work_dir="$HOME/linux-course/shell/test data"
mkdir -p "$work_dir"
cd "$work_dir"
```

若不加双引号，空格会让一个路径变成多个参数。

---

## 二十、变量与命令替换

Shell 脚本章节会系统讲解变量。本章先掌握交互命令所需的基本用法。

### 1. 定义变量

```bash
course_dir="$HOME/linux-course/shell"
```

等号两侧不能有空格。

使用变量：

```bash
cd "$course_dir"
pwd
```

### 2. 查看环境变量

```bash
echo "$HOME"
echo "$USER"
echo "$PATH"
```

### 3. 命令替换

`$(...)` 会执行括号内的命令，并把标准输出替换到当前位置：

```bash
current_dir=$(pwd)
echo "current directory: $current_dir"
```

生成带日期的文件名：

```bash
report_name="report-$(date +%F).txt"
echo "$report_name"
```

`date +%F` 输出类似 `2026-09-28`。

---

## 二十一、组合执行命令

### 1. 分号`;`

```bash
pwd; ls
```

前一条命令无论成功还是失败，后一条都会执行。

### 2. 逻辑与`&&`

```bash
mkdir -p output/report && cd output/report
```

只有左侧命令成功，右侧才执行。需要按顺序完成依赖步骤时使用 `&&`。

### 3. 逻辑或`||`

```bash
grep ERROR logs/system.log || echo "no error found"
```

只有左侧命令失败，右侧才执行。

### 4. 查看退出状态

每条命令结束后都会返回退出状态。`0` 通常表示成功，非零表示失败。

```bash
grep ERROR logs/system.log
echo $?
```

紧接着执行的 `echo $?` 才能看到上一条命令的状态，因为每条新命令都会更新 `$?`。

### 5. 组合示例

```bash
mkdir -p output/summary && \
grep -E 'WARN|ERROR' logs/system.log > output/summary/alerts.log && \
echo "report generated"
```

行末的反斜杠表示命令在下一行继续。任何一步失败，后续由 `&&` 连接的步骤都不会执行。

---

## 二十二、获取命令帮助

真正掌握命令行，不是记住全部选项，而是能快速查到正确用法。

### 1. `--help`

```bash
ls --help
grep --help
```

适合快速查看命令格式和选项列表。

### 2. man手册

```bash
man grep
```

常见手册结构：

- `NAME`：命令名称和一句话说明
- `SYNOPSIS`：调用格式
- `DESCRIPTION`：详细行为
- `OPTIONS`：选项
- `EXAMPLES`：示例，部分手册包含
- `SEE ALSO`：相关命令和文档

`man` 使用与 `less` 相似的操作方式：

| 按键 | 作用 |
| --- | --- |
| `/word` | 搜索关键词 |
| `n` | 下一个匹配 |
| `N` | 上一个匹配 |
| `q` | 退出 |

### 3. help查看Shell内建命令

`cd` 等 Shell 内建命令使用：

```bash
help cd
help type
```

### 4. whatis查看简短说明

```bash
whatis grep
whatis find
```

若系统尚未生成手册索引，`whatis` 可能没有结果，此时直接使用 `man`。

### 5. apropos按功能搜索

```bash
apropos "copy files"
```

当知道任务但不知道命令名时，可以从手册描述中搜索相关命令。

---

## 二十三、命令历史与编辑

### 1. 查看历史

```bash
history
```

### 2. 重新执行历史命令

- `↑`：向前浏览历史。
- `↓`：向后浏览历史。
- `Ctrl + R`：反向搜索历史。

按 `Ctrl + R` 后输入部分内容，例如 `grep`，Shell 会查找最近包含该内容的命令。按 Enter 立即执行，按左右方向键进入编辑。

### 3. 常用编辑快捷键

| 快捷键 | 作用 |
| --- | --- |
| `Ctrl + A` | 移到行首 |
| `Ctrl + E` | 移到行尾 |
| `Ctrl + U` | 删除光标前内容 |
| `Ctrl + K` | 删除光标后内容 |
| `Ctrl + W` | 删除光标前一个单词 |
| `Ctrl + C` | 取消当前输入或中断前台命令 |
| `Ctrl + L` | 清屏 |

命令历史可能保存路径、地址和参数，不应把密码、访问令牌或私钥直接写入命令行。

---

## 二十四、综合实践：生成系统日志报告

### 实践目标

从 `logs/system.log` 中提取告警，统计日志级别，并把结果保存为报告。整个过程只使用本章命令。

### 第1步：确认环境

```bash
cd ~/linux-course/shell
pwd
ls -l logs/system.log
```

查看原始日志：

```bash
cat -n logs/system.log
```

### 第2步：提取告警和错误

```bash
grep -E 'WARN|ERROR' logs/system.log | tee output/alerts.log
```

验证：

```bash
wc -l output/alerts.log
cat output/alerts.log
```

结果应包含两行。

### 第3步：统计各日志级别

日志级别位于每行第三个字段。执行：

```bash
cut -d ' ' -f 3 logs/system.log | sort | uniq -c
```

输出类似：

```text
      1 ERROR
      3 INFO
      1 WARN
```

将结果保存：

```bash
cut -d ' ' -f 3 logs/system.log | sort | uniq -c > output/level-count.txt
```

### 第4步：生成汇总报告

```bash
report="output/report-$(date +%F).txt"
```

写入标题：

```bash
printf "System Log Report\nGenerated: %s\n\n" "$(date '+%F %T')" > "$report"
```

追加统计：

```bash
printf "Log level count:\n" >> "$report"
cat output/level-count.txt >> "$report"
```

追加告警：

```bash
printf "\nAlerts:\n" >> "$report"
cat output/alerts.log >> "$report"
```

查看完整报告：

```bash
cat "$report"
```

### 第5步：复制报告到备份目录

先查看即将复制的文件：

```bash
printf '%s\n' output/report-*.txt
```

确认后复制：

```bash
cp -i output/report-*.txt backup/
```

### 第6步：检查最终文件

```bash
find output backup -maxdepth 1 -type f -print
```

使用 Windows 文件资源管理器打开结果目录：

```bash
cd ~/linux-course/shell
explorer.exe .
```

> **图片占位：** WSL 终端显示日志级别统计与完整报告内容，Windows 文件资源管理器显示 `output` 和 `backup` 中的报告文件。

### 实践问题

1. 为什么 `grep -E 'WARN|ERROR'` 使用单引号？
2. 为什么 `sort` 必须放在 `uniq -c` 前面？
3. `>` 与 `>>` 在报告生成过程中分别承担什么作用？
4. 如果日志文件不存在，错误信息会通过哪个标准通道输出？
5. 如何把生成报告时的正常输出和错误信息分别保存？

---

## 二十五、常见问题

### 命令提示command not found

依次检查：

```bash
type 命令名
command -v 命令名
echo "$PATH"
```

可能原因包括命令拼写错误、软件未安装或可执行文件不在 `PATH` 中。

### cp或mv提示目标不是目录

一次操作多个源文件时，最后一个参数必须是已经存在的目录：

```bash
cp file1 file2 backup/
```

使用以下命令确认目标：

```bash
ls -ld backup
```

### rm提示Is a directory

普通 `rm` 用于删除文件。空目录使用 `rmdir`；包含内容的练习目录只有在明确检查后才使用 `rm -r`。

### 通配符没有匹配到预期文件

检查：

1. 当前目录是否正确。
2. 文件名大小写是否一致。
3. 隐藏文件是否以 `.` 开头。
4. 通配符是否被引号阻止展开。

预览展开结果：

```bash
printf '%s\n' 模式
```

### grep没有输出

`grep` 没找到匹配行时通常保持安静，并返回非零状态。查看：

```bash
grep pattern file
echo $?
```

如果只关心是否存在，可以使用：

```bash
grep -q pattern file
```

### 重定向后终端没有输出

这是重定向的预期结果。检查目标文件：

```bash
cat 输出文件
```

需要同时显示和保存时使用 `tee`。

### 2>&1的顺序为什么重要

下面的命令先让标准输出指向文件，再让标准错误跟随标准输出：

```bash
command > all.log 2>&1
```

若先执行 `2>&1`，标准错误会先跟随当时仍指向终端的标准输出，随后只有标准输出被改到文件。Shell 从左到右处理重定向。

### 文件名包含空格导致参数数量错误

给完整路径加双引号：

```bash
cp "test data/report.txt" output/
```

变量路径也应加双引号：

```bash
cp "$source_file" "$target_dir/"
```

---

## 本章小结

Shell 在执行命令前会处理引号、变量、通配符、管道和重定向。命令接收到的是 Shell 展开后的参数，因此正确使用引号和预览通配符结果，是安全操作文件的基础。

`cp`、`mv`、`rm` 负责文件复制、移动和删除；`cat`、`less`、`head`、`tail` 和 `wc` 负责查看与统计文本；`find` 查找路径，`grep` 搜索内容。标准输入、标准输出和标准错误让不同命令能够通过管道与重定向组成数据处理流程。

掌握这些工具后，你已经可以在终端中整理项目、筛选日志并生成报告。下一章将解释这些文件为什么有不同的所有者和权限，以及 `Permission denied` 应该如何定位。

---

## 本章检查点

- 能区分命令、短选项、长选项和参数。
- 能使用 `type`、`command -v` 判断命令来源。
- 能安全使用 `cp`、`mv`、`rm` 和 `rmdir`。
- 能根据文件长度选择 `cat`、`less`、`head` 或 `tail`。
- 能解释 `*`、`?`、`[]` 和花括号展开的区别。
- 能用 `find` 按名称与类型查找文件。
- 能用 `grep` 显示行号、忽略大小写、反向匹配和递归搜索。
- 能解释标准输入、标准输出、标准错误及其文件描述符。
- 能说明 `>`、`>>`、`<`、`2>`、`2>&1` 和 `|` 的作用。
- 能使用 `tee` 同时显示并保存输出。
- 能正确使用单引号、双引号和反斜杠。
- 能使用 `&&` 和 `||` 根据命令结果控制后续执行。
- 能通过 `--help`、`man` 和 `help` 查询命令用法。
- 能独立完成日志筛选、统计和报告生成。

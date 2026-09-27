# Linux系列

Linux 是嵌入式开发的重要工作环境，也是许多嵌入式设备本身所运行的系统。本系列从终端操作开始，逐步进入文件系统、权限、进程、网络、编译工具和交叉编译，最终建立嵌入式 Linux 的整体认识。

## 学习目标

完成本系列后，你应能够：

- 在 Linux 终端中完成日常文件与目录操作。
- 理解用户、权限、进程和服务的基本管理方式。
- 使用 SSH 连接开发板或服务器并传输文件。
- 使用 GCC、Make、CMake 和 GDB 构建、检查和调试 C 程序。
- 编写简单 Shell 脚本完成重复任务。
- 理解交叉编译工具链以及嵌入式 Linux 系统的组成。

## 推荐学习顺序

```text
环境认识 → 文件系统 → Shell → 权限与用户 → 软件包
         → 进程与服务 → 网络与远程连接
         → Linux开发工具链 → Shell脚本
         → 交叉编译 → 嵌入式Linux概览
```

前七章解决 Linux 的日常使用问题，后四章面向嵌入式软件开发。每章都应在真实终端中完成命令练习，不要只阅读命令说明。

```{toctree}
:maxdepth: 1

start
filesystem
shell
permission
package
process
network
toolchain
script
cross_compile
embedded

```

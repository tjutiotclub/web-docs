# 进程、任务与系统服务

程序运行后形成进程。Linux 通过进程、信号和服务管理长期运行的任务。

## 学习目标

- 区分程序、进程和线程。
- 查看进程及其 PID。
- 管理前台和后台任务。
- 使用信号结束或控制进程。
- 查看 systemd 服务状态和系统日志。

## 查看进程

```bash
ps
top
pgrep
```

本节介绍 PID、父进程、用户、状态和资源占用等基本信息。

## 前台与后台任务

介绍命令末尾的 `&`，以及 `jobs`、`fg`、`bg` 和终端关闭对任务的影响。

## 信号

通过 `kill` 介绍 SIGINT、SIGTERM 和 SIGKILL。正常结束进程应优先使用可被程序处理的终止信号。

## 持续运行

介绍 `nohup`、终端会话与长期服务的区别，为后续 systemd 学习建立基础。

## systemd服务

```bash
systemctl status service
systemctl start service
systemctl stop service
systemctl enable service
```

说明启动、停止、开机启用和查看状态之间的区别。

## 日志

使用 `journalctl` 查看系统与服务日志，并结合 `tail -f` 持续观察普通日志文件。

## 本章实践

启动一个持续运行的测试程序，将其切换到后台，查找 PID，发送正常终止信号，并查看相关状态变化。

## 本章检查点

- 能通过 PID 找到并结束指定进程。
- 能解释前台任务、后台任务和系统服务的区别。
- 能从服务状态和日志中寻找启动失败原因。

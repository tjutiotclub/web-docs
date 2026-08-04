# Vscode C/C++开发环境配置

本章节将逐步讲解如何在 **VS Code** 编辑环境中配置 **C/C++ 开发工具链**。  
由于 VS Code 本身只是代码编辑器，并不具备编译能力，对于像 C/C++ 这样的编译型语言，需要开发者手动配置编译环境和工具链。  
本文将介绍如何搭建 **VS Code + CMake + MinGW/WinLib GCC** 的一体化开发环境，以实现从编辑到编译的完整流程。

---

## 1.下载编译器

我们本次教学使用 **WinLibs GCC**，它是一个专门为 Windows 系统提供的预编译 **GCC（MinGW-w64）** 工具链。

操作步骤如下：

1. 打开 [WinLibs 官网](https://winlibs.com/)。

2. 页面下滑到 **MSVCRT runtime** 类别，选择最新的 **win64 版本工具包** 进行下载。

下载页会随版本更新而变化，请根据自己的系统架构选择 64 位工具链。

---

## 2.安装编译器

1. 下载完成后，找到压缩包文件，例如 `winlibs-x86_64-posix-seh-gcc-12.2.0-9.0.0.zip`。  

2. 右键选择 **解压到指定文件夹**，例如 `E:\Program Files\mingw64`。  

3. 确认文件夹中存在如下结构（示例）：  

```powershell
   PS E:\Program Files\mingw64> ls



       目录: E:\Program Files\mingw64

   Mode                 LastWriteTime         Length Name

   ----                 -------------         ------ ----

   d-----         2026/2/14      0:36                bin
   d-----         2026/2/14      0:36                include
   d-----         2026/2/14      0:36                lib
   d-----         2026/2/14      0:36                libexec
   d-----         2026/2/14      0:36                share
   d-----         2026/2/14      0:36                x86_64-w64-mingw32
   -a----        2025/12/24      4:44            786 mingwvars.bat
   -a----        2025/12/24      4:44            691 version_info.txt

```

---

## 3.配置系统环境变量

为了使Windows系统和Vscode可以顺利识别到**GCC 编译器**，我们需要将GCC编译器的有关路径添加到系统环境变量
以作者的安装路径` E:\Program Files\mingw64`为例。

1. 按 **Win + R**，输入 `sysdm.cpl`回车，打开系统属性，找到`高级选项栏`，进入右下角的`环境变量`子菜单

2. 将安装路径下的bin文件夹路径的绝对路径`E:\Program Files\mingw64\bin`添加到**系统环境变量**下属的**Path**变量

3. 保存关闭
4. 打开PowerShell或CMD，输入以下指令验证GCC编译器是否可以被正常识别

```powershell
gcc --version
```

若命令输出 GCC 的版本信息，说明工具链已加入 `Path`。

---

## 4.配置Vscode开发环境

1.安装相关插件

- **C/C++** （微软官方插件，提供 IntelliSense、调试支持）    

> **提示**：插件安装完成后，需要重启 VS Code 以确保生效。

2.创建C/C++工程文件

使用Vscode打开选定的工程文件夹，创建下属文件main.c输入以下代码

```c
#include <stdio.h>

int main()
{
    printf("Hello, VS Code + GCC!\n");
    return 0;
}
```

3.按**Ctrl + ~**打开Vscode终端，输入指令

```powershell
gcc main.c -o main.exe
```

运行完成后左侧资源管理器中生成`main.exe`可执行文件

4.执行`.\main.exe`观察程序运行结果

```powershell
PS E:\vscode_project\c_cpp\demo> .\main.exe
Hello, VS Code + GCC!
PS E:\vscode_project\c_cpp\demo> 
```

---

> 到此为止，我们已经完成了Vscode的基本配置。
> 
> 接下来的章节中，我们将会引入Cmake对复杂项目进行项目文件管理。

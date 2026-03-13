# Vscode中Cmake的应用

在上一章节中，我们已经能够在 VS Code 中编写 C/C++ 源文件，
并通过如下命令完成编译：

```bash
gcc main.c -o main.exe
```

这种方式适用于简单程序，但当项目规模扩大后，会逐渐暴露出问题：

源文件数量增多

文件之间存在依赖关系

需要不同的编译选项

构建与调试流程难以维护

继续手动编写编译命令将变得低效且容易出错。

因此，我们需要一种更加规范、自动化的方式来管理工程构建，
这就是 CMake 的作用。

在本章节中，我们将学习如何在 VS Code 中借助 CMake
完成项目的配置与构建。

---

## 1.什么是CMake

CMake 是一种 **构建系统生成工具**。  

它并不直接负责编译，而是根据工程描述，  
为不同平台生成对应的构建方案，然后调用编译器完成工作。

在我们的环境中：

CMake → 生成构建流程  
GCC → 执行真正的编译

---

## 2.CMake工程的基本结构

一个最基本的 CMake 工程通常包括：

- 源文件  
- 头文件  
- 一个 `CMakeLists.txt` 用来描述如何构建  

这个文件可以理解为：

**告诉 CMake：哪些文件参与编译，最终要生成什么。**

---

## 3.什么是CMakeLists.txt

`CMakeLists.txt` 是 **:contentReference[oaicite:0]{index=0}** 使用的工程描述文件。

可以将它理解为：

用来告诉 CMake：  

> 这个工程有哪些源文件，  
> 要生成什么目标，  
> 使用什么编译方式。

CMake 本身并不直接编译代码，  
而是通过读取 `CMakeLists.txt`，生成构建流程，  
再调用底层编译器（如 GCC）完成实际编译。

在一个 CMake 工程中：

- **CMakeLists.txt 是必须存在的**
- 工程的构建规则由它统一描述
- VS Code、CMake Tools 等工具，都会以它作为入口

---

## 4. CMakeLists.txt 的基本内容与含义

在自动生成的 CMake 工程中，  
你通常会看到类似如下的内容：

```cmake
cmake_minimum_required(VERSION 3.20)

project(HelloC)

add_executable(HelloC
    main.c
)
```

### 4.1 cmake_minimum_required

`cmake_minimum_required(VERSION 3.20)`

用于声明 **构建该工程所需的最低 CMake 版本**。

这行代码的作用是：

* 防止使用过旧的 CMake 导致构建失败

* 明确工程的构建环境要求

一般由工具自动生成，不需要手动修改。 

### 4.2 project

`project(HelloC)`

用于定义工程名称。

该名称通常会：

* 作为工程的标识

* 影响生成的目标名称

* 在 VS Code 与构建输出中显示

工程名不一定等同于最终生成的文件名，但通常保持一致。 

### 4.3 add_executable

`add_executable(HelloC main.c)`

用于声明：

> 生成一个可执行文件  
> 名称为 `HelloC`  
> 参与编译的源文件为 `main.c`

当工程包含多个源文件时，只需在此处列出即可，  
无需手动拼接复杂的编译命令。

---

## 5. 现代化 CMake 用法：自动收集源文件与头文件

---

在实际工程中，随着源文件数量的增加，手动维护 `add_executable` 中的文件列表会变得非常繁琐。  
现代 CMake 提供了更灵活的方式：
    # 1. 创建可执行目标（先创建一个“空壳”）
    add_executable(test1)
    # 2. 自动收集 core/src 下的所有 C / C++ 源文件
    file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS
        ${CMAKE_CURRENT_SOURCE_DIR}/core/src/*.c
        ${CMAKE_CURRENT_SOURCE_DIR}/core/src/*.cpp
    )

    # 3. 把源文件加入目标
    target_sources(test1 PRIVATE ${SRC_FILES})

    # 4. 添加头文件搜索路径
    target_include_directories(test1 PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/core/inc
    )

    # 5. （可选）指定语言标准
    set_target_properties(test1 PROPERTIES
        C_STANDARD 11
        CXX_STANDARD 17
    )

### 5.1 file(GLOB_RECURSE)

`file(GLOB_RECURSE SRC_FILES …)` 的作用是：

* 遍历指定目录及其子目录，查找符合条件的文件

* 将找到的源文件存入变量 `SRC_FILES`

* `CONFIGURE_DEPENDS` 表示 **当文件增减时，CMake 会自动重新配置**

这样，当你在 `core/src` 添加新的源文件或删除文件时，只需重新配置一次 CMake，即可生效。

* * *

### 5.2 target_sources

`target_sources(test1 PRIVATE ${SRC_FILES})` 表示：

* 将收集到的源文件加入 `test1` 可执行目标

* `PRIVATE` 表示这些源文件仅属于 `test1`，不会影响其他目标

* * *

### 5.3 target_include_directories

`target_include_directories(test1 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/core/inc)` 表示：

* 添加头文件搜索路径

* 代码中可以直接使用 `#include "xxx.h"`

* PRIVATE 意味着仅对当前目标有效

* * *

### 5.4 set_target_properties

可以显式指定语言标准：

* C 文件使用 C11

* C++ 文件使用 C++17

这有助于：

* 保证不同编译器下的统一行为

* 避免默认标准变化带来的兼容问题

* * *

6. VS Code 中的 CMake 应用

----------------------

在 VS Code 中使用 CMake 时，推荐配合 **CMake Tools 插件**：

1. 打开项目文件夹

2. 插件会自动检测 `CMakeLists.txt`

3. 选择一个可用的 Kit（编译器，如 x86 GCC）

4. 点击 **Build** → CMake 会根据配置生成构建文件并调用 GCC

5. 点击 **Run** → 执行生成的可执行文件

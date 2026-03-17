# STM32系列教程0——基本工程搭建

---

各位同学，从本篇文章开始，我们将逐步学习 HAL 库与 STM32CubeMX 在 STM32 系列 MCU 中的使用。

本系列教程基于我校自主设计的 STM32F1 学习板。

源代码链接：[下载仓库 · cc0717/STM32例程 - Gitee.com](https://gitee.com/cc0717/stm32-routine/repository/archive/master.zip) 

相关工具版本：

- STM32CubeMX：6.21.3+

- keil MDK-ARM：5.43.0.0

- C Compiler：ArmClang V6.24

---

在常规嵌入式系统设计课程中，我们通常使用标准库进行程序设计。然而，由于标准库存在架构局限性、代码移植困难等问题，其官方维护已于 2016 年停止。  

在当前开发中，开发者多选择 HAL 库或 LL 库作为替代。其中，HAL 库因配合自动初始化配置工具，广泛用于入门学习。本章将介绍如何使用 STM32CubeMX（以下简称 CubeMX）创建一个最基础的芯片工程。CubeMX 由意法半导体官方开发，暂无中文支持，但掌握基础英语词汇即可顺利使用。

---

## STEP1.选择芯片

1.打开CubeMX后，在入口页面，我们可以清晰的看到主页中央的“ACCESS TO MCU SELECTOR”字样，点击即可进入MCU选择器，开始选择MCU型号。

![1](E:\web-docs\source\stm32\pic\1.png)

2.进入MCU选择器后，搜索 STM32F103RCT6，选择芯片，开始工程：

![2](E:\web-docs\source\stm32\pic\2.png)

## STEP2.时钟配置

1.在 System Core下选择RCC选项，在RCC mode and Configuration中的High Speed Clock(HSE)下选择Crystal/Ceramic Resonator；

![3](E:\web-docs\source\stm32\pic\3.png)

2.点击顶部的 Clock Configuration，进行主频配置，将HCLK(MHZ)设置为于下方蓝字相同数值，程序会自动把MCU设置为全速运行状态；

![4](E:\web-docs\source\stm32\pic\4.png)

## STEP3.Debug端口设置

点击顶部的 Pinout & Configuartion，选择SYS，在Debug下拉框中选择Serial Wire；

![5](E:\web-docs\source\stm32\pic\5.png)

## STEP4.项目设置

1.点击顶部的 Project Manager，给工程起名，选择存放目录，在Toolchain/IDE中选择MDK-ARM；

![6](E:\web-docs\source\stm32\pic\6.png)

2.点击旁边的 Code Generator，勾选Copy only the necessary library files 以及 Generate peripheral initialization as a pair of ‘.c/.h’ files per peripheral；

![7](E:\web-docs\source\stm32\pic\7.png)

## STEP5.生成项目

点击顶部的GENERATE CODE，等待代码生成，打开工程。

![8](E:\web-docs\source\stm32\pic\8.png)

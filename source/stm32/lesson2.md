# STM32系列课程2——LED点亮与熄灭

源代码链接：[下载仓库 · cc0717/STM32例程 - Gitee.com](https://gitee.com/cc0717/stm32-routine/repository/archive/master.zip)

相关工具版本：

* STM32CubeMX：6.21.3+

* keil MDK-ARM：5.43.0.0

* C Compiler：ArmClang V6.24

---

学习内容：

1.LED灯基本知识

2.GPIO在CubeMX中的配置方法与原理

3.LED灯点亮与熄灭的具体实现方法与扩展

---

## 一、基础知识

### 1.什么是LED灯

LED（Light Emitting Diode，发光二极管）是一种半导体发光器件。当电流从阳极流向阴极时，器件内部发生电子与空穴复合，从而释放能量并以光的形式表现出来。

在正常工作范围内，LED 具有如下特性：

* 电流越大，发光亮度越高

* 当电流超过额定值时，会导致器件发热加剧，从而缩短使用寿命，严重时可能烧毁

常见的 LED 颜色包括：红色、黄色、绿色、蓝色及白色等。

### 2. LED压降与电流特性

LED 在正向导通时会产生一定的电压降，称为正向压降（Forward Voltage，Vf）。该参数主要由半导体材料决定，不同颜色的 LED 对应不同的压降范围。

| 颜色  | 压降范围（Vf）    | 说明        |
| --- | ----------- | --------- |
| 红色  | 1.8 – 2.2 V | 低压降       |
| 黄色  | 1.9 – 2.3 V | 接近红色      |
| 绿色  | 2.0 – 3.2 V | 分两种类型（见下） |
| 蓝色  | 2.8 – 3.5 V | 高压降       |
| 白色  | 2.8 – 3.5 V | 蓝光LED+荧光粉 |

注意（重要）：

* 绿色LED存在两种类型：
  
  * 传统绿光：≈2.1V
  
  * 新型高亮绿：≈3.0V

* 实际设计应参考具体器件数据手册

### 3. 插件LED与贴片LED

根据封装形式不同，LED 可分为插件式（DIP）和贴片式（SMD）。两者在电气特性（如正向压降）上基本一致，但在电流承受能力及应用场景上存在差异。

#### （1）插件LED（直插）

* 常见规格：3mm / 5mm

* 额定电流：10–20 mA

* 最大工作电流：一般不超过 20 mA

#### （2）贴片LED（SMD）

根据封装尺寸不同，电流能力差异较大：

| 类型  | 常见封装        | 推荐电流     |
| --- | ----------- | -------- |
| 小功率 | 0603 / 0805 | 5–20 mA  |
| 中功率 | 2835 / 3528 | 30–60 mA |
| 大功率 | 1W以上        | 350 mA+  |

### 4.限流电阻计算

LED必须串联限流电阻，否则会因电流过大损坏。

在实际设计中，为提高LED可靠性，通常不会按最大额定电流工作，而是取约 **70%~80%** 作为工作电流。

因此可将公式简化为：

$$
R=\frac{Vcc-V_f}{0.75Imax}
$$

其中：

* Vcc​：电源电压

* Vf​：LED正向压降

* Imax​：LED标称最大电流

**补充说明**

* 系数 **0.75** 为工程经验值，用于降低实际工作电流，提高LED寿命与稳定性

* 实际设计中，也可以直接使用**期望工作电流 I** 进行计算

* 计算得到的电阻值通常不是标准阻值，应选择**大于计算值的最接近标准电阻**作为最终值

---

## 二、STM32中的GPIO配置

### 1.GPIO时钟

在 STM32F103RCT6 中，GPIO 外设的工作依赖于系统时钟，而时钟的分配与芯片内部总线结构密切相关。该系列单片机采用基于 AMBA 2.0 的片上总线架构，将内核、存储器以及各类外设连接在一起。

在这一架构中，AHB 用于连接内核、存储器和高速资源，APB 用于连接大多数片上外设。APB 又分为 APB1 和 APB2；具体外设的总线归属应以芯片参考手册中的时钟树和 RCC 寄存器说明为准。

在 STM32F103RCT6 中，GPIO 端口挂接在 APB2 上。芯片最高以 72 MHz 系统时钟运行时，APB1 最高为 36 MHz，APB2 最高为 72 MHz。APB2 时钟会影响寄存器访问，但引脚的输出边沿和可用信号速率还受到 GPIO 速度配置、负载、电源和布线等因素影响，不能只由总线频率推断。

需要注意的是，GPIO 外设在上电后其时钟默认是关闭的，必须通过复位与时钟控制器（RCC）手动开启对应端口的时钟，否则对其寄存器的访问将不会生效。因此，在进行 GPIO 配置之前，必须首先完成时钟使能操作，例如：

```c
__HAL_RCC_GPIOA_CLK_ENABLE();
```

该操作的本质，是为 APB2 总线上的 GPIO 模块提供时钟信号，使其能够正常参与系统工作。

### 2. 配置流程

在完成 GPIO 时钟使能之后，需要对引脚的工作方式进行配置。在基于 HAL 库的开发中，GPIO 的初始化主要通过 `GPIO_InitTypeDef` 结构体来实现。用户只需对结构体中的关键参数进行设置，即可完成对 GPIO 工作模式、电气特性及速度的配置。

#### 2.1 GPIO_InitTypeDef结构体参数说明

GPIO初始化结构体包含以下几个成员

```c
typedef struct
{
  uint32_t Pin;        // 引脚号
  uint32_t Mode;       // 工作模式
  uint32_t Pull;       // 上拉/下拉
  uint32_t Speed;      // 输出速度
} GPIO_InitTypeDef;
```

各参数含义如下：

##### 2.1.1 Pin（引脚号）

在 STM32F103RCT6 中，每个 GPIO 端口（如 GPIOA、GPIOB 等）均包含 16 个引脚，编号为 0～15，因此对应为 PA0～PA15、PB0～PB15 等。

`Pin` 参数用于指定需要初始化的引脚编号，可以选择单个引脚，也可以通过按位或（`|`）同时选择多个引脚。

其定义如下所示：

```c
#define GPIO_PIN_0                 ((uint16_t)0x0001)  /* Pin 0 selected    */
#define GPIO_PIN_1                 ((uint16_t)0x0002)  /* Pin 1 selected    */
#define GPIO_PIN_2                 ((uint16_t)0x0004)  /* Pin 2 selected    */
#define GPIO_PIN_3                 ((uint16_t)0x0008)  /* Pin 3 selected    */
#define GPIO_PIN_4                 ((uint16_t)0x0010)  /* Pin 4 selected    */
#define GPIO_PIN_5                 ((uint16_t)0x0020)  /* Pin 5 selected    */
#define GPIO_PIN_6                 ((uint16_t)0x0040)  /* Pin 6 selected    */
#define GPIO_PIN_7                 ((uint16_t)0x0080)  /* Pin 7 selected    */
#define GPIO_PIN_8                 ((uint16_t)0x0100)  /* Pin 8 selected    */
#define GPIO_PIN_9                 ((uint16_t)0x0200)  /* Pin 9 selected    */
#define GPIO_PIN_10                ((uint16_t)0x0400)  /* Pin 10 selected   */
#define GPIO_PIN_11                ((uint16_t)0x0800)  /* Pin 11 selected   */
#define GPIO_PIN_12                ((uint16_t)0x1000)  /* Pin 12 selected   */
#define GPIO_PIN_13                ((uint16_t)0x2000)  /* Pin 13 selected   */
#define GPIO_PIN_14                ((uint16_t)0x4000)  /* Pin 14 selected   */
#define GPIO_PIN_15                ((uint16_t)0x8000)  /* Pin 15 selected   */
#define GPIO_PIN_All               ((uint16_t)0xFFFF)  /* All pins selected */
```

这些宏定义的本质是**位掩码(bit mask)** 格式，每一位对应一个引脚。例如：

* `GPIO_PIN_0` 对应二进制 `0000 0000 0000 0001`

* `GPIO_PIN_1` 对应二进制 `0000 0000 0000 0010`

因此，可以通过按位或运算同时选择多个引脚，例如：

```c
GPIO_InitStruct.Pin = GPIO_PIN_5 | GPIO_PIN_6;
```

上述配置表示同时初始化PA5和PA6。

##### 2.1.2 Mode（工作模式）与 Pull（上拉/下拉/悬空）

在 STM32F103RCT6 中，`Mode` 参数用于配置 GPIO 引脚的工作方式，是 GPIO 初始化中最核心的参数。通过该参数，可以决定引脚是作为输入、输出，还是由片上外设接管（复用功能）。

从本质上看，GPIO 的工作模式是由其内部寄存器（CRL/CRH）中的控制位决定的，不同模式对应不同的电气特性和功能组合。在 HAL 库中，这些配置被封装为统一的宏定义，便于用户使用。

###### 2.1.2.1 模式分类

GPIO的工作模式可以从功能上划分为三大类：

- 通用输入输出模式：输入模式（Input），输出模式（Output）

- 复用功能模式（Alternate Function）

- 模拟模式（Analog）

在实际应用中，这些模式进一步组合，形成常用的八种工作方式。

###### 2.1.2.2 GPIO的八大工作模式

1.输出模式

GPIO的输出模式有四种，两两一组，分为推挽输出和开漏输出，以及复用推挽输出和复用开漏输出。

其程序内部定义如下：

```c
#define  GPIO_MODE_OUTPUT_PP                    0x00000001u   /*!< Output Push Pull Mode                 */
#define  GPIO_MODE_OUTPUT_OD                    0x00000011u   /*!< Output Open Drain Mode                */
#define  GPIO_MODE_AF_PP                        0x00000002u   /*!< Alternate Function Push Pull Mode     */
#define  GPIO_MODE_AF_OD                        0x00000012u   /*!< Alternate Function Open Drain Mode    */
```

推挽输出（GPIO_MODE_OUTPUT_PP ）可以主动输出高电平（Vpp）与低电平（Vdd），由MCU内部的上下管实现互补驱动。该驱动模式具有驱动能力强（最大驱动电流20mA）与电平反转速度快的特点。常用于LED驱动与普通数字输出。

开漏输出（GPIO_MODE_OUTPUT_OD）与推挽输出不同，其内部仅包含下拉晶体管，当输出低电平时，由 MCU 主动拉低引脚；而当需要输出高电平时，下拉管关闭，引脚处于高阻态，此时电平由外部上拉电阻决定。

这种结构的特点是：

* 只能主动输出低电平，高电平依赖外部电路

* 可实现“线与”（wired-AND）功能

* 支持多个设备共享同一信号线

复用功能模式包括复用推挽输出（GPIO_MODE_AF_PP）和复用开漏输出（GPIO_MODE_AF_OD）。与普通输出模式不同，这两种模式下 GPIO 引脚的控制权不再由 CPU 直接操作，而是交由片上外设（如串口、SPI、I2C、定时器等）接管。

其中，“推挽”与“开漏”的电气特性与前述普通输出模式完全一致，因此不再赘述。复用模式的核心在于：**GPIO 从通用 I/O 转变为专用外设接口引脚**。

在复用推挽输出（GPIO_MODE_AF_PP）模式下，引脚由外设驱动，并采用推挽结构输出信号，具有驱动能力强、速度快的特点，适用于大多数数字通信接口，如串口发送（USART_TX）、SPI 时钟（SCK）等。

在复用开漏输出（GPIO_MODE_AF_OD）模式下，引脚同样由外设控制，但输出结构为开漏形式，需依赖外部上拉电阻形成高电平。该模式主要用于需要“线与”特性的通信接口，例如 I2C 总线中的 SDA 和 SCL 信号。

需要理解的是，复用模式的本质是**功能复用**：同一个物理引脚可以在不同配置下承担不同外设功能，这也是 STM32 引脚资源复用能力的重要体现。因此，开漏输出常用于总线型通信场合，如 I2C 等需要多设备协同工作的场景。

2.输入模式

GPIO 的常用输入模式包括上拉输入、下拉输入、悬空输入以及模拟输入四种。这四种输入方式由 `Mode` 与 `Pull` 参数共同配置实现。

对于 USART_RX 等外设输入引脚，STM32F1 通常按照外设要求配置为浮空输入或上拉输入；具体配置应查阅对应外设章节和数据手册中的引脚说明。

其程序内部定义如下：

```c
#define  GPIO_MODE_INPUT                        0x00000000u   /*!< Input Floating Mode                   */
#define  GPIO_MODE_ANALOG                       0x00000003u   /*!< Analog Mode  */

#define  GPIO_NOPULL        0x00000000u   /*!< No Pull-up or Pull-down activation  */
#define  GPIO_PULLUP        0x00000001u   /*!< Pull-up activation                  */
#define  GPIO_PULLDOWN      0x00000002u   /*!< Pull-down activation                */
```

在输入模式下，GPIO 引脚主要用于采集外部信号，其电气特性由内部是否连接上拉或下拉电阻决定。根据 `Mode` 与 `Pull` 参数的不同组合，可以形成以下四种常用输入方式。

悬空输入（GPIO_MODE_INPUT + GPIO_NOPULL）是指引脚既不连接上拉电阻，也不连接下拉电阻，此时引脚处于高阻态，其电平完全由外部信号决定。当引脚未连接有效信号源时，电平容易受到外界干扰而发生随机变化，因此一般仅在外部电路已经提供稳定驱动的情况下使用。

上拉输入（GPIO_MODE_INPUT + GPIO_PULLUP）是在引脚内部接入上拉电阻，使引脚在无外部输入时默认保持高电平。当外部电路将引脚拉低时，输入状态发生改变。该模式具有良好的抗干扰能力，是按键输入、电平检测等场景中最常用的配置方式。

下拉输入（GPIO_MODE_INPUT + GPIO_PULLDOWN）是在引脚内部接入下拉电阻，使引脚在无外部输入时默认保持低电平。当外部输入为高电平时，引脚状态发生变化。该模式适用于需要默认低电平的输入场合，其原理与上拉输入类似。

模拟输入（GPIO_MODE_ANALOG）用于关闭 GPIO 的数字输入输出缓冲电路，使引脚直接连接到片上的模拟模块（如 ADC）。在该模式下，引脚不参与数字逻辑判断，从而有效降低功耗，并减少数字电路对模拟信号的干扰。因此，在进行模数转换或低功耗设计时，应优先选择该模式。

###### 2.1.2.3配置示例

综上，我们给出输入/输出工作模式的配置代码片段参考：

**1. 推挽输出**

```c
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  
GPIO_InitStruct.Pull = GPIO_NOPULL; 
```

**2. 开漏输出**

```c
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;  
GPIO_InitStruct.Pull = GPIO_NOPULL;   // 如需输出高电平，通常需外接上拉电阻 
```

**3. 复用推挽输出**

```c
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;  
GPIO_InitStruct.Pull = GPIO_NOPULL; 
```

**4. 复用开漏输出**

```c
GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;  
GPIO_InitStruct.Pull = GPIO_NOPULL;   // 如需输出高电平，通常需外接上拉电阻 
```

**5. 悬空输入**

```c
GPIO_InitStruct.Mode = GPIO_MODE_INPUT;  
GPIO_InitStruct.Pull = GPIO_NOPULL; 
```

**6. 上拉输入**

```c
GPIO_InitStruct.Mode = GPIO_MODE_INPUT;  
GPIO_InitStruct.Pull = GPIO_PULLUP; 
```

**7. 下拉输入**

```c
GPIO_InitStruct.Mode = GPIO_MODE_INPUT;  
GPIO_InitStruct.Pull = GPIO_PULLDOWN; 
```

**8. 模拟输入**

```c
GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;  
GPIO_InitStruct.Pull = GPIO_NOPULL;
```

##### 2.1.3 Speed（输出速度）

在完成 GPIO 工作模式配置后，对于输出模式或复用模式，还需要进一步配置引脚的输出速度参数。`Speed` 参数用于控制 GPIO 引脚的驱动能力和电平翻转速度，是影响信号质量的重要因素之一。

在 STM32F103RCT6 中，GPIO 的输出速度本质上对应的是引脚内部驱动电路的响应能力，其程序定义如下：

```c
#define GPIO_SPEED_FREQ_LOW       0x00000002u   /*!< Low speed      */
#define GPIO_SPEED_FREQ_MEDIUM    0x00000001u   /*!< Medium speed   */
#define GPIO_SPEED_FREQ_HIGH      0x00000003u   /*!< High speed     */
```

需要注意的是，这里的“速度”并非指信号的通信速率，而是指 GPIO 输出电平从低到高或从高到低的变化速度（即上升沿和下降沿的快慢）。

###### 2.1.3.1 速度等级说明

在 STM32F1 系列中，GPIO 输出速度通常对应以下三个等级：

* 低速（Low Speed）：约 2 MHz

* 中速（Medium Speed）：约 10 MHz

* 高速（High Speed）：约 50 MHz

这里的 MHz 是 STM32F1 对输出模式速度等级的标称值，主要反映输出驱动与边沿速度，并不保证引脚能够在相同频率下稳定输出方波。实际可用速率还取决于负载、电源、布线和信号完整性。

###### 2.1.3.2 Speed 参数的作用

GPIO 输出速度主要影响以下几个方面：

**① 信号上升沿/下降沿速度**  

速度越高，引脚电平变化越快，适用于高速数字信号输出。

**② 驱动能力**  

较高的速度对应更强的驱动能力，可以带动更大的负载。

**③ 电磁干扰（EMI）**  

速度越高，信号边沿越陡，可能带来更强的电磁干扰。

###### 2.1.3.3 实际使用建议

在实际应用中，应根据具体需求合理选择 GPIO 输出速度：

| 应用场景           | 推荐速度  |
| -------------- | ----- |
| LED 控制         | 低速或中速 |
| 普通IO输出         | 中速    |
| 高速通信（SPI、时钟信号） | 高速    |

一般情况下，不建议默认全部配置为高速模式，以避免不必要的功耗增加和电磁干扰问题。

###### 2.1.3.4 配置示例

```c
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
```

该配置表示将 GPIO 引脚设置为高速输出模式，适用于对响应速度要求较高的场景。

#### 2.2 GPIO初始化的使用方法（HAL_GPIO_Init）

在前一节中，我们已经介绍了 GPIO 配置所需的各项参数（`Pin`、`Mode`、`Pull`、`Speed`）。在实际开发中，这些参数需要组合使用，并通过 `HAL_GPIO_Init` 函数完成初始化配置。

GPIO 初始化的基本使用流程如下。 

##### 2.2.1定义初始化结构体

```c
GPIO_InitTypeDef GPIO_InitStruct = {0};
```

该结构体用于存放 GPIO 的各项配置参数。 

##### 2.2.2配置引脚及工作模式

根据实际需求，对结构体成员进行赋值。例如配置 PA5 为推挽输出：

```c
GPIO_InitStruct.Pin = GPIO_PIN_5;  
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  
GPIO_InitStruct.Pull = GPIO_NOPULL;  
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH; 
```

##### 2.2.3调用初始化函数

HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

执行该函数后，相关配置将写入 GPIO 寄存器，引脚开始按照设定方式工作。 

##### 2.2.4完整示例

```c
GPIO_InitTypeDef GPIO_InitStruct = {0};  

/* 1. 开启GPIOA时钟 */  
__HAL_RCC_GPIOA_CLK_ENABLE();  

/* 2. 配置引脚参数 */  
GPIO_InitStruct.Pin = GPIO_PIN_5;  
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  
GPIO_InitStruct.Pull = GPIO_NOPULL;  
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;  

/* 3. 初始化GPIO */  
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

```

---

## 三、CubeMX中配置GPIO

在第二部分中，我们已经介绍了GPIO配置的相关参数及其实现方法。

本章将基于上述原理，借助CubeMX工具完成GPIO引脚的快速配置过程，
并建立“图形化配置”与“代码实现”之间的对应关系。

关于如何建立CubeMX工程文件及完成基本系统配置，
已在《STM32系列课程0》中进行说明，这里不再赘述。

实验所使用的教学板上预装有8个LED灯珠，
本次将以LED1（PA4）为例进行说明。

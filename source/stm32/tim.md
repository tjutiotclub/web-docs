# TIM函数介绍

本文所列函数并非HAL库中全部TIM相关函数，而是日常开发中最常用、最基础的操作函数。这些函数已经能够满足绝大多数定时器的使用需求，包括**基本计数、定时中断、PWM输出、输入捕获及编码器模式**，适用于入门学习与一般工程应用。

本文重点整理**定时器运行时控制相关函数**（如启动、停止、中断及数据读取等），用于快速查表与实际开发调用。

对于更复杂的功能（如复用功能配置、高级定时器控制、同步触发等），可在此基础上进一步查阅HAL库官方文档进行扩展。

<mark>说明：</mark>  
<mark>1. 定时器初始化（如分频、计数周期等）通常由CubeMX自动生成（如MX_TIMx_Init），本文不涉及初始化配置函数</mark>  
<mark>2. 本文不包含DMA相关函数，DMA属于进阶功能，不影响基础定时器使用</mark>  
<mark>3. 本文不包含Output Compare、One Pulse及高级控制功能，这些功能使用频率较低或属于进阶应用</mark>  
<mark>4. 本文不包含MSP相关函数（底层硬件初始化），该部分通常由CubeMX自动生成</mark>



## 定时器中断基本使用流程

```c
// 1. 初始化定时器（CubeMX已生成）

// 2. 启动定时器（带中断）
HAL_TIM_Base_Start_IT(&htim1);

// 3. 回调函数
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if(htim == &htim1)
    {
        // TODO
    }
}

```

---

## HAL_TIM_Base_Start函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_Base_Start(TIM_HandleTypeDef *htim)
```

| 函数名       | HAL_TIM_Base_Start               |
| --------- | -------------------------------- |
| 函数作用      | 启动定时器（基础计数功能，不开启中断）              |
| 返回值       | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim | 定时器句柄指针，用于指定要启动的定时器              |

应用示例：

```c
HAL_TIM_Base_Start(&htim1); // 启动定时器1（不使能中断）
```

<mark>注意：该函数仅启动定时器计数，不会触发中断，如需中断功能应使用HAL_TIM_Base_Start_IT</mark>

---

## HAL_TIM_Base_Stop函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_Base_Stop(TIM_HandleTypeDef *htim)
```

| 函数名       | HAL_TIM_Base_Stop                |
| --------- | -------------------------------- |
| 函数作用      | 停止定时器（基础计数功能，不涉及中断）              |
| 返回值       | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim | 定时器句柄指针，用于指定要停止的定时器              |

应用示例：

```c
HAL_TIM_Base_Stop(&htim1); // 停止定时器1
```

<mark>注意：该函数仅停止定时器计数，如之前使用中断方式启动（Start_IT），需使用HAL_TIM_Base_Stop_IT关闭中断</mark>

---

## HAL_TIM_Base_Start_IT函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_Base_Start_IT(TIM_HandleTypeDef *htim)
```

| 函数名       | HAL_TIM_Base_Start_IT            |
| --------- | -------------------------------- |
| 函数作用      | 启动定时器，并开启更新中断（周期性触发中断）           |
| 返回值       | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim | 定时器句柄指针，用于指定要启动的定时器              |

应用示例：

```c
HAL_TIM_Base_Start_IT(&htim1); // 启动定时器1并开启中断
```

<mark>注意：使用该函数后，定时器溢出将进入HAL_TIM_PeriodElapsedCallback回调函数</mark>

---

## HAL_TIM_Base_Stop_IT函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_Base_Stop_IT(TIM_HandleTypeDef *htim)
```

| 函数名       | HAL_TIM_Base_Stop_IT             |
| --------- | -------------------------------- |
| 函数作用      | 停止定时器，并关闭更新中断                    |
| 返回值       | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim | 定时器句柄指针，用于指定要停止的定时器              |

应用示例：

```c
HAL_TIM_Base_Stop_IT(&htim1); // 停止定时器1并关闭中断
```

<mark>注意：该函数用于关闭由HAL_TIM_Base_Start_IT开启的定时器中断</mark>

---

## HAL_TIM_PeriodElapsedCallback函数

函数原型：

```c
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim);
```

| 函数名       | HAL_TIM_PeriodElapsedCallback |
| --------- | ----------------------------- |
| 函数作用      | 定时器周期性中断回调函数                  |
| 返回值       | void                          |
| 参数1：*htim | 触发中断的定时器指针，无需用户输入             |

应用实例：

```c
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if(htim == &htim1)//判断是哪个定时器触发
    {
        //TODO:定时器1中断触发执行的内容
    }

}
```

<mark>注意：该函数为弱函数，需要用户自行重写</mark>

--- 

## 脉冲宽度调制（PWM）

---

HAL_TIM_PWM_Start函数
-------------------

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_PWM_Start(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_PWM_Start                |
| ----------- | -------------------------------- |
| 函数作用        | 启动指定通道的PWM输出（不带中断）               |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim   | 定时器句柄指针，用于指定定时器                  |
| 参数2：Channel | 指定PWM输出通道（如TIM_CHANNEL_1~4）      |

应用示例：

```c
HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1); // 启动TIM1通道1的PWM输出
```

<mark>注意：该函数仅启动PWM输出，不会产生中断</mark>

* * *

HAL_TIM_PWM_Stop函数
------------------

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_PWM_Stop(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_PWM_Stop                 |
| ----------- | -------------------------------- |
| 函数作用        | 停止指定通道的PWM输出                     |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim   | 定时器句柄指针，用于指定定时器                  |
| 参数2：Channel | 指定PWM输出通道（如TIM_CHANNEL_1~4）      |

应用示例：

```c
HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_1); // 停止TIM1通道1的PWM输出
```

<mark>注意：该函数用于关闭由HAL_TIM_PWM_Start启动的PWM输出</mark>

* * *

HAL_TIM_PWM_Start_IT函数
----------------------

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_PWM_Start_IT(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_PWM_Start_IT             |
| ----------- | -------------------------------- |
| 函数作用        | 启动指定通道的PWM输出，并开启中断               |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim   | 定时器句柄指针，用于指定定时器                  |
| 参数2：Channel | 指定PWM输出通道（如TIM_CHANNEL_1~4）      |

应用示例：

```c
HAL_TIM_PWM_Start_IT(&htim1, TIM_CHANNEL_1); // 启动PWM并开启中断
```

<mark>注意：开启中断后，可在对应PWM回调函数中处理事件</mark>

* * *

HAL_TIM_PWM_Stop_IT函数
---------------------

函数原型：

```c
 HAL_StatusTypeDef HAL_TIM_PWM_Stop_IT(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_PWM_Stop_IT              |
| ----------- | -------------------------------- |
| 函数作用        | 停止指定通道的PWM输出，并关闭中断               |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim   | 定时器句柄指针，用于指定定时器                  |
| 参数2：Channel | 指定PWM输出通道（如TIM_CHANNEL_1~4）      |

应用示例：

```c
HAL_TIM_PWM_Stop_IT(&htim1, TIM_CHANNEL_1); // 停止PWM并关闭中断
```

<mark>注意：该函数用于关闭由HAL_TIM_PWM_Start_IT开启的PWM及其中断</mark>

* * *

__HAL_TIM_SET_COMPARE函数
-----------------------

函数原型：

```c
#define __HAL_TIM_SET_COMPARE(__HANDLE__, __CHANNEL__, __COMPARE__)
```

| 函数名             | __HAL_TIM_SET_COMPARE         |
| --------------- | ----------------------------- |
| 函数作用            | 设置指定通道的比较值（CCR寄存器），用于控制PWM占空比 |
| 返回值             | 无（宏定义）                        |
| 参数1：**HANDLE**  | 定时器句柄（如&htim1）                |
| 参数2：**CHANNEL** | 指定通道（如TIM_CHANNEL_1~4）        |
| 参数3：**COMPARE** | 比较值（决定占空比，范围通常为0~ARR）         |

应用示例：

```c
__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, 500); // 设置占空比（比较值为500）
```

<mark>注意：占空比 = CCR / ARR，例如ARR=1000，CCR=500时，占空比为50%</mark>

---

## 输入捕获（Input Capture）

---

### HAL_TIM_IC_Start函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_IC_Start(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_IC_Start                 |
| ----------- | -------------------------------- |
| 函数作用        | 启动指定通道的输入捕获（不带中断）                |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim   | 定时器句柄指针，用于指定定时器                  |
| 参数2：Channel | 指定输入捕获通道（如TIM_CHANNEL_1~4）       |

应用示例：

```c
HAL_TIM_IC_Start(&htim1, TIM_CHANNEL_1); // 启动TIM1通道1输入捕获
```

<mark>注意：该函数不会触发中断，需手动读取捕获值</mark>

* * *

### HAL_TIM_IC_Stop函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_IC_Stop(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_IC_Stop                  |
| ----------- | -------------------------------- |
| 函数作用        | 停止指定通道的输入捕获                      |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim   | 定时器句柄指针，用于指定定时器                  |
| 参数2：Channel | 指定输入捕获通道（如TIM_CHANNEL_1~4）       |

应用示例：

```c
HAL_TIM_IC_Stop(&htim1, TIM_CHANNEL_1); // 停止输入捕获
```

* * *

### HAL_TIM_IC_Start_IT函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_IC_Start_IT(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_IC_Start_IT              |
| ----------- | -------------------------------- |
| 函数作用        | 启动输入捕获，并开启捕获中断                   |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim   | 定时器句柄指针                          |
| 参数2：Channel | 指定输入捕获通道                         |

应用示例：

```c
HAL_TIM_IC_Start_IT(&htim1, TIM_CHANNEL_1); // 启动输入捕获中断
```

<mark>注意：捕获事件发生时会进入HAL_TIM_IC_CaptureCallback回调函数</mark>

* * *

HAL_TIM_IC_Stop_IT函数
--------------------

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_IC_Stop_IT(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_IC_Stop_IT               |
| ----------- | -------------------------------- |
| 函数作用        | 停止输入捕获，并关闭中断                     |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim   | 定时器句柄指针                          |
| 参数2：Channel | 指定输入捕获通道                         |

应用示例：

```c
HAL_TIM_IC_Stop_IT(&htim1, TIM_CHANNEL_1); // 停止输入捕获中断
```

* * *

### HAL_TIM_IC_CaptureCallback函数

函数原型：

```c
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
```

| 函数名       | HAL_TIM_IC_CaptureCallback |
| --------- | -------------------------- |
| 函数作用      | 输入捕获中断回调函数                 |
| 返回值       | void                       |
| 参数1：*htim | 触发捕获的定时器指针                 |

应用示例：

```c
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)  
{  
    if(htim == &htim1)  
    {  
        // TODO: 处理捕获数据  
    }  
}
```

<mark>注意：该函数为弱函数，需要用户自行重写</mark>

* * *

### HAL_TIM_ReadCapturedValue函数

函数原型：

```c
uint32_t HAL_TIM_ReadCapturedValue(const TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_ReadCapturedValue |
| ----------- | ------------------------- |
| 函数作用        | 读取指定通道的捕获值（CCR寄存器值）       |
| 返回值         | 捕获到的计数值（uint32_t）         |
| 参数1：*htim   | 定时器句柄指针                   |
| 参数2：Channel | 指定输入捕获通道                  |

应用示例：

```c
uint32_t value = HAL_TIM_ReadCapturedValue(&htim1, TIM_CHANNEL_1);
```

<mark>注意：该值为当前计数器捕获值，通常用于计算周期或频率</mark>

---

## 编码器模式（Encoder）

* * *

### HAL_TIM_Encoder_Start函数

函数原型：

HAL_StatusTypeDef HAL_TIM_Encoder_Start(TIM_HandleTypeDef *htim, uint32_t Channel)

| 函数名         | HAL_TIM_Encoder_Start            |
| ----------- | -------------------------------- |
| 函数作用        | 启动编码器接口（不带中断）                    |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim   | 定时器句柄指针，用于指定定时器                  |
| 参数2：Channel | 指定通道（通常为TIM_CHANNEL_ALL）         |

应用示例：

HAL_TIM_Encoder_Start(&htim1, TIM_CHANNEL_ALL); // 启动编码器模式

<mark>注意：编码器模式通常同时使用CH1和CH2通道</mark>

* * *

### HAL_TIM_Encoder_Stop函数

函数原型：

HAL_StatusTypeDef HAL_TIM_Encoder_Stop(TIM_HandleTypeDef *htim, uint32_t Channel)

| 函数名         | HAL_TIM_Encoder_Stop             |
| ----------- | -------------------------------- |
| 函数作用        | 停止编码器接口                          |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim   | 定时器句柄指针                          |
| 参数2：Channel | 指定通道（通常为TIM_CHANNEL_ALL）         |

应用示例：

HAL_TIM_Encoder_Stop(&htim1, TIM_CHANNEL_ALL); // 停止编码器

* * *

### HAL_TIM_Encoder_Start_IT函数

函数原型：

HAL_StatusTypeDef HAL_TIM_Encoder_Start_IT(TIM_HandleTypeDef *htim, uint32_t Channel)

| 函数名         | HAL_TIM_Encoder_Start_IT         |
| ----------- | -------------------------------- |
| 函数作用        | 启动编码器接口，并开启中断                    |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示启动成功） |
| 参数1：*htim   | 定时器句柄指针                          |
| 参数2：Channel | 指定通道（通常为TIM_CHANNEL_ALL）         |

应用示例：

```c
HAL_TIM_Encoder_Start_IT(&htim1, TIM_CHANNEL_ALL); // 启动编码器（中断模式）
```

<mark>注意：一般编码器模式不依赖中断，通常直接读取计数值</mark>

* * *

### HAL_TIM_Encoder_Stop_IT函数

函数原型：

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Stop_IT(TIM_HandleTypeDef *htim, uint32_t Channel)
```

| 函数名         | HAL_TIM_Encoder_Stop_IT          |
| ----------- | -------------------------------- |
| 函数作用        | 停止编码器接口，并关闭中断                    |
| 返回值         | HAL_StatusTypeDef（如HAL_OK表示停止成功） |
| 参数1：*htim   | 定时器句柄指针                          |
| 参数2：Channel | 指定通道（通常为TIM_CHANNEL_ALL）         |

应用示例：

```c
HAL_TIM_Encoder_Stop_IT(&htim1, TIM_CHANNEL_ALL); // 停止编码器（中断模式）
```

* * *

### __HAL_TIM_GET_COUNTER宏定义

函数原型：

```c
#define __HAL_TIM_GET_COUNTER(__HANDLE__)
```

| 名称             | __HAL_TIM_GET_COUNTER |
| -------------- | --------------------- |
| 类型             | 宏定义                   |
| 作用             | 读取当前定时器计数值（CNT寄存器）    |
| 返回值            | 当前计数值（uint32_t）       |
| 参数1：**HANDLE** | 定时器句柄（如&htim1）        |

应用示例：

```c
int16_t cnt = __HAL_TIM_GET_COUNTER(&htim1); // 获取当前计数值
```

<mark>注意：计数值会随编码器旋转方向自动增减</mark>

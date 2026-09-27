# ADC函数介绍

本文整理 STM32 HAL 库中最常用的 ADC 操作函数，包括**校准、启动转换、轮询采样、中断采样和 DMA 采样**。这些函数已经能够满足电位器、光敏电阻、红外传感器等常见模拟量采集需求。

ADC 的通道、采样时间、连续转换模式和数据对齐方式通常由 CubeMX 完成配置。本文重点说明初始化完成后，程序如何启动转换并取得结果。

<mark>说明：</mark>

<mark>1. 本文以 STM32F103C8T6 的 HAL 库为例，ADC 分辨率为 12 位，转换结果通常为 0~4095</mark>

<mark>2. 输入电压不得超过芯片允许范围，通常应位于 0~VDDA 之间</mark>

<mark>3. 使用 DMA 前，需要在 CubeMX 中为 ADC 添加 DMA 通道</mark>

## ADC轮询采样基本流程

```c
uint32_t adc_value;

HAL_ADCEx_Calibration_Start(&hadc1); // F1系列建议先校准
HAL_ADC_Start(&hadc1);               // 启动转换

if(HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK)
{
    adc_value = HAL_ADC_GetValue(&hadc1);
}

HAL_ADC_Stop(&hadc1);                // 停止ADC
```

---

## HAL_ADCEx_Calibration_Start函数

函数原型：

```c
HAL_StatusTypeDef HAL_ADCEx_Calibration_Start(ADC_HandleTypeDef *hadc)
```

| 函数名 | HAL_ADCEx_Calibration_Start |
| --- | --- |
| 函数作用 | 启动 ADC 自校准，减小转换误差 |
| 返回值 | HAL_StatusTypeDef，如 HAL_OK 表示校准成功 |
| 参数1：*hadc | ADC 句柄指针，如 &hadc1 |

应用示例：

```c
if(HAL_ADCEx_Calibration_Start(&hadc1) != HAL_OK)
{
    Error_Handler();
}
```

<mark>注意：该函数是 STM32F1 HAL 的扩展函数。通常在 ADC 初始化完成后、第一次启动转换前调用一次即可</mark>

---

## HAL_ADC_Start函数

函数原型：

```c
HAL_StatusTypeDef HAL_ADC_Start(ADC_HandleTypeDef *hadc)
```

| 函数名 | HAL_ADC_Start |
| --- | --- |
| 函数作用 | 启动 ADC 规则组转换，不开启中断或 DMA |
| 返回值 | HAL_StatusTypeDef，如 HAL_OK 表示启动成功 |
| 参数1：*hadc | ADC 句柄指针 |

应用示例：

```c
HAL_ADC_Start(&hadc1); // 启动ADC1转换
```

<mark>注意：启动成功不代表转换已经完成，随后应等待转换完成再读取数据</mark>

---

## HAL_ADC_PollForConversion函数

函数原型：

```c
HAL_StatusTypeDef HAL_ADC_PollForConversion(ADC_HandleTypeDef *hadc, uint32_t Timeout)
```

| 函数名 | HAL_ADC_PollForConversion |
| --- | --- |
| 函数作用 | 轮询等待 ADC 转换完成 |
| 返回值 | HAL_OK 表示转换完成，HAL_TIMEOUT 表示等待超时 |
| 参数1：*hadc | ADC 句柄指针 |
| 参数2：Timeout | 最大等待时间，单位为 ms；HAL_MAX_DELAY 表示一直等待 |

应用示例：

```c
if(HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK)
{
    uint32_t value = HAL_ADC_GetValue(&hadc1);
}
```

<mark>注意：该函数会阻塞当前程序，实时性要求较高或采样量较大时应考虑中断或 DMA</mark>

---

## HAL_ADC_GetValue函数

函数原型：

```c
uint32_t HAL_ADC_GetValue(ADC_HandleTypeDef *hadc)
```

| 函数名 | HAL_ADC_GetValue |
| --- | --- |
| 函数作用 | 读取最近一次 ADC 规则组转换结果 |
| 返回值 | ADC 转换结果 |
| 参数1：*hadc | ADC 句柄指针 |

应用示例：

```c
uint32_t adc_value = HAL_ADC_GetValue(&hadc1);
float voltage = adc_value * 3.3f / 4095.0f;
```

<mark>注意：3.3 V 只是示例参考电压。实际换算应使用电路中真实的 VDDA，并确认 CubeMX 中的数据对齐方式</mark>

---

## HAL_ADC_Stop函数

函数原型：

```c
HAL_StatusTypeDef HAL_ADC_Stop(ADC_HandleTypeDef *hadc)
```

| 函数名 | HAL_ADC_Stop |
| --- | --- |
| 函数作用 | 停止以普通轮询方式启动的 ADC 转换 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hadc | ADC 句柄指针 |

应用示例：

```c
HAL_ADC_Stop(&hadc1);
```

---

## ADC中断采样

### HAL_ADC_Start_IT函数

函数原型：

```c
HAL_StatusTypeDef HAL_ADC_Start_IT(ADC_HandleTypeDef *hadc)
```

| 函数名 | HAL_ADC_Start_IT |
| --- | --- |
| 函数作用 | 启动 ADC 转换并开启转换完成中断 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hadc | ADC 句柄指针 |

应用示例：

```c
HAL_ADC_Start_IT(&hadc1);
```

### HAL_ADC_ConvCpltCallback函数

函数原型：

```c
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc)
```

| 函数名 | HAL_ADC_ConvCpltCallback |
| --- | --- |
| 函数作用 | ADC 转换完成回调函数 |
| 返回值 | void |
| 参数1：*hadc | 触发回调的 ADC 句柄指针，由程序自动传入 |

应用示例：

```c
volatile uint32_t adc_value;

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc)
{
    if(hadc == &hadc1)
    {
        adc_value = HAL_ADC_GetValue(hadc);
    }
}
```

<mark>注意：该函数为弱函数，需要用户自行重写。回调函数在中断环境中执行，不应在其中进行长时间延时或阻塞操作</mark>

### HAL_ADC_Stop_IT函数

```c
HAL_StatusTypeDef HAL_ADC_Stop_IT(ADC_HandleTypeDef *hadc)
```

用于停止由 `HAL_ADC_Start_IT` 启动的转换并关闭相关中断。

```c
HAL_ADC_Stop_IT(&hadc1);
```

---

## ADC的DMA采样

### HAL_ADC_Start_DMA函数

函数原型：

```c
HAL_StatusTypeDef HAL_ADC_Start_DMA(ADC_HandleTypeDef *hadc,
                                    uint32_t *pData,
                                    uint32_t Length)
```

| 函数名 | HAL_ADC_Start_DMA |
| --- | --- |
| 函数作用 | 启动 ADC 转换，并由 DMA 自动搬运转换结果 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hadc | ADC 句柄指针 |
| 参数2：*pData | 接收数据缓冲区指针 |
| 参数3：Length | 需要搬运的数据个数，而不是字节数 |

应用示例：

```c
uint32_t adc_buffer[16];

HAL_ADC_Start_DMA(&hadc1, adc_buffer, 16);
```

<mark>注意：STM32F1 HAL 的参数类型为 uint32_t *。DMA 的数据宽度、循环模式以及 ADC 的扫描和连续转换模式必须与采样目标相匹配</mark>

### HAL_ADC_Stop_DMA函数

```c
HAL_StatusTypeDef HAL_ADC_Stop_DMA(ADC_HandleTypeDef *hadc)
```

应用示例：

```c
HAL_ADC_Stop_DMA(&hadc1);
```

该函数用于停止 ADC 的 DMA 传输，并关闭相关 DMA 请求。

---

## 多通道采样说明

使用扫描模式采集多个通道时，需要在 CubeMX 中为每个通道设置不同的 Rank，并使 DMA 缓冲区长度与通道数量或采样序列长度对应。例如 ADC1 配置 3 个规则通道后：

```c
uint32_t adc_value[3];

HAL_ADC_Start_DMA(&hadc1, adc_value, 3);
```

此时 `adc_value[0]`、`adc_value[1]`、`adc_value[2]` 分别对应三个 Rank 的转换结果。若 DMA 使用 Circular 模式，缓冲区会被持续更新。

---

## 常见问题

- **采样值一直为 0 或 4095**：检查引脚是否配置为 Analog、输入电压是否超出范围、通道是否选择正确。
- **采样值波动较大**：检查模拟地、参考电压、信号源阻抗和采样时间，必要时进行多次采样平均。
- **多通道数据顺序不对**：检查 CubeMX 中各通道的 Rank 顺序。
- **DMA 只执行一次**：检查 DMA 是否配置为 Circular，以及 ADC 是否开启连续转换。
- **函数返回 HAL_BUSY**：检查上一次转换是否停止，或是否混用了轮询、中断和 DMA 启动方式。

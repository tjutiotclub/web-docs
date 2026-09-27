# HAL通用函数介绍

在学习 GPIO、定时器、ADC 和通信外设之前，需要先理解所有 HAL 驱动共同使用的基础规则。本章整理**返回状态、延时、系统节拍和非阻塞计时**。这些内容不会由 CubeMX 根据某个外设配置自动写入用户业务逻辑，却会在后续示例中反复使用。

<mark>说明：HAL 初始化、系统时钟、外设初始化和 NVIC 配置属于 CubeMX 工程生成与开发板教学内容，本文不重复讲解</mark>

---

## HAL_StatusTypeDef返回状态

许多 HAL 函数都会返回 `HAL_StatusTypeDef`：

```c
typedef enum
{
    HAL_OK      = 0x00U,
    HAL_ERROR   = 0x01U,
    HAL_BUSY    = 0x02U,
    HAL_TIMEOUT = 0x03U
} HAL_StatusTypeDef;
```

| 返回状态 | 含义 |
| --- | --- |
| HAL_OK | 操作成功 |
| HAL_ERROR | 外设或参数状态导致操作失败 |
| HAL_BUSY | 外设正在执行上一次操作 |
| HAL_TIMEOUT | 在规定时间内没有完成操作 |

不要默认每次调用都会成功。对于初始化、通信和启动函数，应至少在调试阶段检查返回值：

```c
HAL_StatusTypeDef status;

status = HAL_UART_Transmit(&huart1, data, data_size, 100);

if(status != HAL_OK)
{
    // 记录错误或进入错误处理
}
```

`HAL_BUSY` 常见于中断或 DMA 操作尚未完成时再次启动同一外设；`HAL_TIMEOUT` 则通常表示从机未响应、接线有误或超时时间过短。

---

## HAL_Delay函数

函数原型：

```c
void HAL_Delay(uint32_t Delay)
```

| 函数名 | HAL_Delay |
| --- | --- |
| 函数作用 | 阻塞当前程序至少指定的毫秒数 |
| 返回值 | void |
| 参数1：Delay | 延时时间，单位为 ms |

应用示例：

```c
HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
HAL_Delay(500);
```

`HAL_Delay` 适合点灯测试、上电等待和简单演示，但程序在延时期间不能继续执行主循环中的其他任务。

<mark>注意：不要在普通外设中断回调中调用 HAL_Delay。默认延时依赖 SysTick 中断，在中断环境中可能无法继续计时并造成程序卡死</mark>

---

## HAL_GetTick函数

函数原型：

```c
uint32_t HAL_GetTick(void)
```

| 函数名 | HAL_GetTick |
| --- | --- |
| 函数作用 | 获取 HAL 启动以来累计的系统节拍 |
| 返回值 | 默认情况下为累计毫秒数 |
| 参数 | 无 |

应用示例：

```c
uint32_t last_toggle = 0;

while(1)
{
    if(HAL_GetTick() - last_toggle >= 500U)
    {
        last_toggle = HAL_GetTick();
        HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
    }

    // 这里还可以执行其他任务
}
```

这种写法不会阻塞主循环，适合多个任务按不同周期运行。

<mark>注意：应使用 `当前值 - 上次值 >= 周期` 的无符号减法形式，不要直接比较绝对结束时间。这样即使计数值溢出，周期判断仍然能够正常工作</mark>

---

## 超时参数与HAL_MAX_DELAY

轮询式通信函数通常带有 `Timeout` 参数，例如：

```c
HAL_UART_Transmit(&huart1, data, size, 100);
HAL_I2C_Master_Receive(&hi2c1, address, data, size, 100);
```

`Timeout` 的单位通常为毫秒，用于限制函数最多阻塞多久。也可以传入：

```c
HAL_MAX_DELAY
```

它表示不主动设置有限等待时间。初学示例中偶尔可以使用，但实际工程不宜在外部设备可能掉线时无限等待，否则一个故障设备就可能阻塞整个程序。

---

## 初学阶段需要掌握的边界

学完本章后，应能够：

- 检查 `HAL_OK`、`HAL_BUSY`、`HAL_TIMEOUT` 等状态。
- 区分阻塞延时与基于 `HAL_GetTick` 的非阻塞计时。
- 正确设置轮询函数的超时时间，避免程序无限等待。

掌握这些内容后，再学习 GPIO、定时器和通信外设时，就不会把每个 HAL 函数看成彼此独立的知识点。

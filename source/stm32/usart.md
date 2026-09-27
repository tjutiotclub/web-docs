# USART函数介绍

本文整理 STM32 HAL 库中最常用的串口函数，包括**阻塞收发、中断收发、DMA 收发、空闲线接收和回调函数**。

STM32 的 USART 支持同步和异步通信；在常见串口项目中通常使用异步模式，因此 HAL 函数统一使用 `HAL_UART_...` 命名，句柄类型为 `UART_HandleTypeDef`。即使 CubeMX 中启用的是 USART1，代码中仍然使用 `huart1` 和 `HAL_UART_Transmit`。

<mark>说明：</mark>

<mark>1. 波特率、数据位、停止位和校验位通常由 CubeMX 配置</mark>

<mark>2. 通信双方的串口参数必须一致，并且必须共地</mark>

<mark>3. USART 的 TX 应连接对方 RX，RX 应连接对方 TX</mark>

## 串口阻塞收发基本流程

```c
uint8_t tx_data[] = "Hello STM32\r\n";
uint8_t rx_data[8];

HAL_UART_Transmit(&huart1, tx_data, sizeof(tx_data) - 1, 100);
HAL_UART_Receive(&huart1, rx_data, sizeof(rx_data), 1000);
```

---

## HAL_UART_Transmit函数

函数原型：

```c
HAL_StatusTypeDef HAL_UART_Transmit(UART_HandleTypeDef *huart,
                                    uint8_t *pData,
                                    uint16_t Size,
                                    uint32_t Timeout)
```

| 函数名 | HAL_UART_Transmit |
| --- | --- |
| 函数作用 | 以阻塞方式发送串口数据 |
| 返回值 | HAL_StatusTypeDef，如 HAL_OK 表示发送成功 |
| 参数1：*huart | 串口句柄指针，如 &huart1 |
| 参数2：*pData | 发送数据缓冲区指针 |
| 参数3：Size | 发送数据的字节数 |
| 参数4：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t message[] = "System ready\r\n";

HAL_UART_Transmit(&huart1,
                  message,
                  sizeof(message) - 1,
                  100);
```

<mark>注意：字符串数组末尾包含 `\0`，因此示例使用 `sizeof(message) - 1`，不发送字符串结束符</mark>

---

## HAL_UART_Receive函数

函数原型：

```c
HAL_StatusTypeDef HAL_UART_Receive(UART_HandleTypeDef *huart,
                                   uint8_t *pData,
                                   uint16_t Size,
                                   uint32_t Timeout)
```

| 函数名 | HAL_UART_Receive |
| --- | --- |
| 函数作用 | 以阻塞方式接收指定数量的串口数据 |
| 返回值 | HAL_OK 表示收满指定数据，HAL_TIMEOUT 表示等待超时 |
| 参数1：*huart | 串口句柄指针 |
| 参数2：*pData | 接收缓冲区指针 |
| 参数3：Size | 期望接收的字节数 |
| 参数4：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t command;

if(HAL_UART_Receive(&huart1, &command, 1, 1000) == HAL_OK)
{
    // 已收到一个字节
}
```

<mark>注意：该函数会等待接收满 Size 个数据或超时。串口数据长度不固定时，更适合使用中断、DMA 或空闲线接收</mark>

---

## HAL_UART_Transmit_IT函数

函数原型：

```c
HAL_StatusTypeDef HAL_UART_Transmit_IT(UART_HandleTypeDef *huart,
                                       uint8_t *pData,
                                       uint16_t Size)
```

| 函数名 | HAL_UART_Transmit_IT |
| --- | --- |
| 函数作用 | 以中断方式启动串口发送，函数不会等待发送完成 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*huart | 串口句柄指针 |
| 参数2：*pData | 发送缓冲区指针 |
| 参数3：Size | 发送数据的字节数 |

应用示例：

```c
uint8_t tx_data[] = "OK\r\n";
HAL_UART_Transmit_IT(&huart1, tx_data, sizeof(tx_data) - 1);
```

发送完成后进入：

```c
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
    if(huart == &huart1)
    {
        // 串口1发送完成
    }
}
```

<mark>注意：发送完成前不能修改或释放 tx_data 缓冲区</mark>

---

## HAL_UART_Receive_IT函数

函数原型：

```c
HAL_StatusTypeDef HAL_UART_Receive_IT(UART_HandleTypeDef *huart,
                                      uint8_t *pData,
                                      uint16_t Size)
```

| 函数名 | HAL_UART_Receive_IT |
| --- | --- |
| 函数作用 | 以中断方式启动串口接收 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*huart | 串口句柄指针 |
| 参数2：*pData | 接收缓冲区指针 |
| 参数3：Size | 本次期望接收的字节数 |

接收单字节并持续重新开启的常见写法：

```c
uint8_t rx_byte;

int main(void)
{
    // HAL_Init、时钟和外设初始化由CubeMX生成
    HAL_UART_Receive_IT(&huart1, &rx_byte, 1);

    while(1)
    {
    }
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if(huart == &huart1)
    {
        // 处理rx_byte，建议只做简单操作

        HAL_UART_Receive_IT(&huart1, &rx_byte, 1); // 重新开启下一次接收
    }
}
```

<mark>注意：普通中断接收完成一次后不会自动重新启动。若要持续接收，必须在回调中再次调用 HAL_UART_Receive_IT</mark>

---

## HAL_UART_Transmit_DMA函数

函数原型：

```c
HAL_StatusTypeDef HAL_UART_Transmit_DMA(UART_HandleTypeDef *huart,
                                        uint8_t *pData,
                                        uint16_t Size)
```

应用示例：

```c
uint8_t tx_buffer[128];
HAL_UART_Transmit_DMA(&huart1, tx_buffer, sizeof(tx_buffer));
```

DMA 发送适合传输较长数据。发送完成后进入 `HAL_UART_TxCpltCallback`，完成前不能修改发送缓冲区。

---

## HAL_UART_Receive_DMA函数

函数原型：

```c
HAL_StatusTypeDef HAL_UART_Receive_DMA(UART_HandleTypeDef *huart,
                                       uint8_t *pData,
                                       uint16_t Size)
```

应用示例：

```c
uint8_t rx_buffer[64];
HAL_UART_Receive_DMA(&huart1, rx_buffer, sizeof(rx_buffer));
```

普通 DMA 接收只有在收满 `Size` 个数据后才调用 `HAL_UART_RxCpltCallback`。如果每帧长度不固定，建议使用空闲线接收。

---

## HAL_UARTEx_ReceiveToIdle_DMA函数

函数原型：

```c
HAL_StatusTypeDef HAL_UARTEx_ReceiveToIdle_DMA(UART_HandleTypeDef *huart,
                                               uint8_t *pData,
                                               uint16_t Size)
```

| 函数名 | HAL_UARTEx_ReceiveToIdle_DMA |
| --- | --- |
| 函数作用 | 启动 DMA 接收，在缓冲区收满或检测到空闲线时报告已接收长度 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*huart | 串口句柄指针 |
| 参数2：*pData | 接收缓冲区指针 |
| 参数3：Size | 缓冲区最大容量 |

应用示例：

```c
uint8_t rx_buffer[64];

HAL_UARTEx_ReceiveToIdle_DMA(&huart1, rx_buffer, sizeof(rx_buffer));
__HAL_DMA_DISABLE_IT(huart1.hdmarx, DMA_IT_HT); // 不需要半传输事件时可关闭

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size)
{
    if(huart == &huart1)
    {
        // rx_buffer[0] 到 rx_buffer[Size - 1] 为本次收到的数据
        // 建议在此处设置标志，随后在主循环中处理数据

        HAL_UARTEx_ReceiveToIdle_DMA(&huart1,
                                     rx_buffer,
                                     sizeof(rx_buffer));
        __HAL_DMA_DISABLE_IT(huart1.hdmarx, DMA_IT_HT);
    }
}
```

<mark>注意：该接口和回调需要较新版本的 STM32F1 HAL。若当前工程中找不到它们，请更新对应 HAL 驱动，或使用 DMA 加空闲线中断的传统实现</mark>

---

## HAL_UART_AbortReceive函数

函数原型：

```c
HAL_StatusTypeDef HAL_UART_AbortReceive(UART_HandleTypeDef *huart)
```

| 函数名 | HAL_UART_AbortReceive |
| --- | --- |
| 函数作用 | 中止当前串口接收，使接收状态恢复为可重新启动 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*huart | 串口句柄指针 |

应用示例：

```c
HAL_UART_AbortReceive(&huart1);
HAL_UART_Receive_IT(&huart1, &rx_byte, 1);
```

当协议状态需要复位或接收发生异常时，可以中止本次接收后重新启动。

---

## HAL_UART_ErrorCallback函数

函数原型：

```c
void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)
```

应用示例：

```c
volatile uint32_t uart_error;

void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)
{
    if(huart == &huart1)
    {
        uart_error = HAL_UART_GetError(huart);
        HAL_UART_Receive_IT(&huart1, &rx_byte, 1);
    }
}
```

常见错误包括奇偶校验错误、噪声错误、帧错误和溢出错误。该函数为弱函数，需要用户自行重写。

---

## printf重定向示例

使用 GCC 工具链时，可以通过重写 `_write` 将 `printf` 输出到串口：

```c
#include <stdio.h>

int _write(int file, char *ptr, int len)
{
    HAL_UART_Transmit(&huart1, (uint8_t *)ptr, len, HAL_MAX_DELAY);
    return len;
}
```

之后即可使用：

```c
printf("ADC value: %lu\r\n", (unsigned long)adc_value);
```

<mark>注意：阻塞式 printf 不适合高频中断或大量实时数据输出。在中断回调中也不应直接使用这种写法</mark>

---

## 常见问题

- **收到乱码**：检查双方波特率、数据位、停止位、校验位以及系统时钟配置。
- **完全收不到数据**：检查 TX/RX 是否交叉连接、是否共地、引脚复用和串口编号是否正确。
- **只能接收一次**：中断或空闲线回调结束前没有重新启动下一次接收。
- **出现 ORE 溢出错误**：程序未及时读取数据，考虑使用中断或 DMA，并减少回调中的耗时操作。
- **异步发送返回 HAL_BUSY**：上一次中断或 DMA 发送尚未完成，应等待发送完成回调。
- **DMA 数据被覆盖**：主循环处理速度跟不上接收速度，应使用双缓冲、环形缓冲区或及时复制有效数据。

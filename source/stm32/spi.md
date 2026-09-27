# SPI函数介绍

本文整理 STM32 HAL 库中最常用的 SPI 函数，包括**阻塞收发、中断收发、DMA 收发、片选控制和回调函数**。

SPI 是同步全双工通信接口，常见信号包括 SCK、MOSI、MISO 和片选 CS。主机通过时钟极性 CPOL 与时钟相位 CPHA 决定采样时序，因此主机配置必须与从机数据手册一致。

<mark>说明：</mark>

<mark>1. SPI 工作模式、数据位宽、波特率分频、CPOL 和 CPHA 通常由 CubeMX 配置</mark>

<mark>2. 普通 GPIO 片选最直观，也最便于在一次完整事务前后精确控制</mark>

<mark>3. SPI 本身没有设备地址和应答机制，读写命令格式由具体器件规定</mark>

## SPI片选基本写法

以下假设片选信号低电平有效：

```c
HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_RESET); // 选中设备
HAL_SPI_Transmit(&hspi1, tx_data, tx_size, 100);
HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_SET);   // 释放设备
```

片选应覆盖一笔完整事务。对于“命令 + 地址 + 数据”连续传输，不应在中间随意拉高片选。

---

## HAL_SPI_Transmit函数

函数原型：

```c
HAL_StatusTypeDef HAL_SPI_Transmit(SPI_HandleTypeDef *hspi,
                                   uint8_t *pData,
                                   uint16_t Size,
                                   uint32_t Timeout)
```

| 函数名 | HAL_SPI_Transmit |
| --- | --- |
| 函数作用 | 以阻塞方式发送 SPI 数据 |
| 返回值 | HAL_StatusTypeDef，如 HAL_OK 表示发送成功 |
| 参数1：*hspi | SPI 句柄指针，如 &hspi1 |
| 参数2：*pData | 发送数据缓冲区指针 |
| 参数3：Size | 发送的数据单元数量 |
| 参数4：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t command = 0x9F;

HAL_GPIO_WritePin(FLASH_CS_GPIO_Port, FLASH_CS_Pin, GPIO_PIN_RESET);
HAL_SPI_Transmit(&hspi1, &command, 1, 100);
HAL_GPIO_WritePin(FLASH_CS_GPIO_Port, FLASH_CS_Pin, GPIO_PIN_SET);
```

<mark>注意：当 SPI 配置为 8 位数据宽度时，Size 表示字节数；配置为 16 位时，Size 表示 16 位数据单元的数量</mark>

---

## HAL_SPI_Receive函数

函数原型：

```c
HAL_StatusTypeDef HAL_SPI_Receive(SPI_HandleTypeDef *hspi,
                                  uint8_t *pData,
                                  uint16_t Size,
                                  uint32_t Timeout)
```

| 函数名 | HAL_SPI_Receive |
| --- | --- |
| 函数作用 | 以阻塞方式接收 SPI 数据 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hspi | SPI 句柄指针 |
| 参数2：*pData | 接收缓冲区指针 |
| 参数3：Size | 接收的数据单元数量 |
| 参数4：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t rx_data[3];
HAL_SPI_Receive(&hspi1, rx_data, 3, 100);
```

<mark>注意：SPI 主机只有产生时钟才能接收数据。HAL 会在接收过程中发送空数据以产生时钟，具体行为与通信方向配置有关</mark>

---

## HAL_SPI_TransmitReceive函数

函数原型：

```c
HAL_StatusTypeDef HAL_SPI_TransmitReceive(SPI_HandleTypeDef *hspi,
                                          uint8_t *pTxData,
                                          uint8_t *pRxData,
                                          uint16_t Size,
                                          uint32_t Timeout)
```

| 函数名 | HAL_SPI_TransmitReceive |
| --- | --- |
| 函数作用 | 以阻塞方式同时发送和接收数据 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hspi | SPI 句柄指针 |
| 参数2：*pTxData | 发送缓冲区指针 |
| 参数3：*pRxData | 接收缓冲区指针 |
| 参数4：Size | 交换的数据单元数量 |
| 参数5：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t tx_data[2] = {0x80, 0xFF};
uint8_t rx_data[2];

HAL_GPIO_WritePin(SENSOR_CS_GPIO_Port, SENSOR_CS_Pin, GPIO_PIN_RESET);
HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 2, 100);
HAL_GPIO_WritePin(SENSOR_CS_GPIO_Port, SENSOR_CS_Pin, GPIO_PIN_SET);
```

SPI 每发送一个数据单元也会接收一个数据单元。某些器件的第一个返回字节无效，应根据器件时序图决定使用接收数组中的哪些数据。

---

## SPI中断收发

### HAL_SPI_Transmit_IT函数

```c
HAL_StatusTypeDef HAL_SPI_Transmit_IT(SPI_HandleTypeDef *hspi,
                                      uint8_t *pData,
                                      uint16_t Size)
```

### HAL_SPI_Receive_IT函数

```c
HAL_StatusTypeDef HAL_SPI_Receive_IT(SPI_HandleTypeDef *hspi,
                                     uint8_t *pData,
                                     uint16_t Size)
```

### HAL_SPI_TransmitReceive_IT函数

```c
HAL_StatusTypeDef HAL_SPI_TransmitReceive_IT(SPI_HandleTypeDef *hspi,
                                             uint8_t *pTxData,
                                             uint8_t *pRxData,
                                             uint16_t Size)
```

以上函数启动传输后立即返回，传输完成后分别进入对应回调：

```c
void HAL_SPI_TxCpltCallback(SPI_HandleTypeDef *hspi)
{
    if(hspi == &hspi1)
    {
        HAL_GPIO_WritePin(FLASH_CS_GPIO_Port, FLASH_CS_Pin, GPIO_PIN_SET);
    }
}

void HAL_SPI_RxCpltCallback(SPI_HandleTypeDef *hspi)
{
    if(hspi == &hspi1)
    {
        // 接收完成
    }
}

void HAL_SPI_TxRxCpltCallback(SPI_HandleTypeDef *hspi)
{
    if(hspi == &hspi1)
    {
        HAL_GPIO_WritePin(SENSOR_CS_GPIO_Port, SENSOR_CS_Pin, GPIO_PIN_SET);
    }
}
```

<mark>注意：使用中断方式时，不要在启动函数返回后立刻释放片选。应在对应完成回调中释放片选</mark>

---

## SPI的DMA收发

### HAL_SPI_Transmit_DMA函数

```c
HAL_StatusTypeDef HAL_SPI_Transmit_DMA(SPI_HandleTypeDef *hspi,
                                       uint8_t *pData,
                                       uint16_t Size)
```

### HAL_SPI_Receive_DMA函数

```c
HAL_StatusTypeDef HAL_SPI_Receive_DMA(SPI_HandleTypeDef *hspi,
                                      uint8_t *pData,
                                      uint16_t Size)
```

### HAL_SPI_TransmitReceive_DMA函数

```c
HAL_StatusTypeDef HAL_SPI_TransmitReceive_DMA(SPI_HandleTypeDef *hspi,
                                              uint8_t *pTxData,
                                              uint8_t *pRxData,
                                              uint16_t Size)
```

应用示例：

```c
uint8_t display_data[128];

HAL_GPIO_WritePin(DISPLAY_CS_GPIO_Port, DISPLAY_CS_Pin, GPIO_PIN_RESET);
HAL_SPI_Transmit_DMA(&hspi1, display_data, sizeof(display_data));
```

DMA 完成后仍会进入相应的 `HAL_SPI_TxCpltCallback`、`HAL_SPI_RxCpltCallback` 或 `HAL_SPI_TxRxCpltCallback`。传输完成前，缓冲区内容和片选状态都必须保持有效。

---

## HAL_SPI_Abort函数

函数原型：

```c
HAL_StatusTypeDef HAL_SPI_Abort(SPI_HandleTypeDef *hspi)
```

| 函数名 | HAL_SPI_Abort |
| --- | --- |
| 函数作用 | 中止正在进行的 SPI 传输，并使外设回到可重新使用的状态 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hspi | SPI 句柄指针 |

应用示例：

```c
if(HAL_SPI_Abort(&hspi1) == HAL_OK)
{
    HAL_GPIO_WritePin(SENSOR_CS_GPIO_Port, SENSOR_CS_Pin, GPIO_PIN_SET);
}
```

中止传输后，还应恢复片选等由用户控制的外部信号。

---

## HAL_SPI_ErrorCallback函数

```c
void HAL_SPI_ErrorCallback(SPI_HandleTypeDef *hspi)
{
    if(hspi == &hspi1)
    {
        uint32_t error = HAL_SPI_GetError(hspi);
        (void)error;
        HAL_GPIO_WritePin(SENSOR_CS_GPIO_Port, SENSOR_CS_Pin, GPIO_PIN_SET);
    }
}
```

该函数为弱函数，需要用户自行重写。常见错误包括溢出、模式错误和 DMA 传输错误。

---

## 常见问题

- **数据全部为 0x00 或 0xFF**：检查片选、MISO 接线、器件供电和读命令格式。
- **数据整体错位**：检查 CPOL、CPHA 和数据位宽是否与从机一致。
- **低速正常、高速异常**：降低波特率，检查连线长度、信号完整性和器件允许的最高时钟。
- **中断或 DMA 只收到一部分数据**：确认缓冲区生命周期、Size 单位和 DMA 配置。
- **第二次调用返回 HAL_BUSY**：前一次异步传输尚未结束，应等待完成回调后再启动下一次传输。

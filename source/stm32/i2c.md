# I2C函数介绍

本文整理 STM32 HAL 库中最常用的 I2C 函数，包括**主机收发、存储器读写、中断与 DMA 收发、设备检测和回调函数**。

I2C 使用 SCL 和 SDA 两根信号线，允许多个设备共享总线。STM32 在常见项目中通常作为主机，通过从机地址访问传感器、EEPROM、OLED 等设备。

<mark>说明：</mark>

<mark>1. I2C 引脚、速率和寻址模式通常由 CubeMX 配置，本文不讲解底层 MSP 初始化</mark>

<mark>2. HAL 函数中的 DevAddress 通常要求传入左移一位后的 8 位地址</mark>

<mark>3. 总线必须具有上拉电阻，许多模块板已经自带，但使用前仍应确认</mark>

## 设备地址说明

器件手册常给出 7 位地址，例如 MPU6050 的地址为 `0x68`。HAL I2C 函数的 `DevAddress` 参数应写为：

```c
#define MPU6050_ADDR (0x68 << 1)
```

读写位由 HAL 库自动处理，不需要手动加 1。若器件手册已经给出 8 位写地址和读地址，则应先判断它采用的是哪一种表示方式，避免重复左移。

## I2C阻塞收发基本流程

```c
uint8_t tx_data[2] = {0x6B, 0x00};
uint8_t rx_data[6];

HAL_I2C_Master_Transmit(&hi2c1, MPU6050_ADDR, tx_data, 2, 100);
HAL_I2C_Master_Receive(&hi2c1, MPU6050_ADDR, rx_data, 6, 100);
```

---

## HAL_I2C_Master_Transmit函数

函数原型：

```c
HAL_StatusTypeDef HAL_I2C_Master_Transmit(I2C_HandleTypeDef *hi2c,
                                          uint16_t DevAddress,
                                          uint8_t *pData,
                                          uint16_t Size,
                                          uint32_t Timeout)
```

| 函数名 | HAL_I2C_Master_Transmit |
| --- | --- |
| 函数作用 | I2C 主机以阻塞方式向从机发送数据 |
| 返回值 | HAL_StatusTypeDef，如 HAL_OK 表示发送成功 |
| 参数1：*hi2c | I2C 句柄指针，如 &hi2c1 |
| 参数2：DevAddress | 从机地址，通常为 7 位地址左移一位 |
| 参数3：*pData | 发送数据缓冲区指针 |
| 参数4：Size | 发送数据的字节数 |
| 参数5：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t data[2] = {0x6B, 0x00};

if(HAL_I2C_Master_Transmit(&hi2c1, 0x68 << 1, data, 2, 100) != HAL_OK)
{
    Error_Handler();
}
```

<mark>注意：该函数会阻塞程序，直到发送完成、出现错误或等待超时</mark>

---

## HAL_I2C_Master_Receive函数

函数原型：

```c
HAL_StatusTypeDef HAL_I2C_Master_Receive(I2C_HandleTypeDef *hi2c,
                                         uint16_t DevAddress,
                                         uint8_t *pData,
                                         uint16_t Size,
                                         uint32_t Timeout)
```

| 函数名 | HAL_I2C_Master_Receive |
| --- | --- |
| 函数作用 | I2C 主机以阻塞方式从从机接收数据 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hi2c | I2C 句柄指针 |
| 参数2：DevAddress | 从机地址，通常为 7 位地址左移一位 |
| 参数3：*pData | 接收缓冲区指针 |
| 参数4：Size | 需要接收的字节数 |
| 参数5：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t data[6];
HAL_I2C_Master_Receive(&hi2c1, 0x68 << 1, data, 6, 100);
```

---

## HAL_I2C_Mem_Write函数

函数原型：

```c
HAL_StatusTypeDef HAL_I2C_Mem_Write(I2C_HandleTypeDef *hi2c,
                                    uint16_t DevAddress,
                                    uint16_t MemAddress,
                                    uint16_t MemAddSize,
                                    uint8_t *pData,
                                    uint16_t Size,
                                    uint32_t Timeout)
```

| 函数名 | HAL_I2C_Mem_Write |
| --- | --- |
| 函数作用 | 向 I2C 设备的指定寄存器或存储地址写入数据 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hi2c | I2C 句柄指针 |
| 参数2：DevAddress | 从机地址 |
| 参数3：MemAddress | 目标寄存器或存储地址 |
| 参数4：MemAddSize | 地址宽度：I2C_MEMADD_SIZE_8BIT 或 I2C_MEMADD_SIZE_16BIT |
| 参数5：*pData | 发送数据缓冲区 |
| 参数6：Size | 写入数据的字节数 |
| 参数7：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t value = 0x00;

HAL_I2C_Mem_Write(&hi2c1,
                  0x68 << 1,
                  0x6B,
                  I2C_MEMADD_SIZE_8BIT,
                  &value,
                  1,
                  100);
```

<mark>注意：MemAddSize 表示寄存器地址本身的宽度，与一次写入多少数据无关</mark>

---

## HAL_I2C_Mem_Read函数

函数原型：

```c
HAL_StatusTypeDef HAL_I2C_Mem_Read(I2C_HandleTypeDef *hi2c,
                                   uint16_t DevAddress,
                                   uint16_t MemAddress,
                                   uint16_t MemAddSize,
                                   uint8_t *pData,
                                   uint16_t Size,
                                   uint32_t Timeout)
```

| 函数名 | HAL_I2C_Mem_Read |
| --- | --- |
| 函数作用 | 从 I2C 设备的指定寄存器或存储地址读取数据 |
| 返回值 | HAL_StatusTypeDef |
| 参数1：*hi2c | I2C 句柄指针 |
| 参数2：DevAddress | 从机地址 |
| 参数3：MemAddress | 目标寄存器或存储地址 |
| 参数4：MemAddSize | 寄存器地址宽度 |
| 参数5：*pData | 接收数据缓冲区 |
| 参数6：Size | 读取数据的字节数 |
| 参数7：Timeout | 最大等待时间，单位为 ms |

应用示例：

```c
uint8_t who_am_i;

HAL_I2C_Mem_Read(&hi2c1,
                 0x68 << 1,
                 0x75,
                 I2C_MEMADD_SIZE_8BIT,
                 &who_am_i,
                 1,
                 100);
```

`HAL_I2C_Mem_Read` 会完成“发送寄存器地址，再读取数据”的组合过程，访问寄存器型设备时通常比手动拼接收发更方便。

---

## HAL_I2C_IsDeviceReady函数

函数原型：

```c
HAL_StatusTypeDef HAL_I2C_IsDeviceReady(I2C_HandleTypeDef *hi2c,
                                        uint16_t DevAddress,
                                        uint32_t Trials,
                                        uint32_t Timeout)
```

| 函数名 | HAL_I2C_IsDeviceReady |
| --- | --- |
| 函数作用 | 检测指定地址的从机是否应答 |
| 返回值 | HAL_OK 表示收到应答 |
| 参数1：*hi2c | I2C 句柄指针 |
| 参数2：DevAddress | 待检测的从机地址 |
| 参数3：Trials | 最大尝试次数 |
| 参数4：Timeout | 每次操作的超时时间，单位为 ms |

应用示例：

```c
if(HAL_I2C_IsDeviceReady(&hi2c1, 0x68 << 1, 3, 100) == HAL_OK)
{
    // 设备在线
}
```

该函数也可用于编写地址扫描程序，但扫描时必须避免越界并正确处理保留地址。

---

## I2C中断收发

```c
HAL_StatusTypeDef HAL_I2C_Master_Transmit_IT(I2C_HandleTypeDef *hi2c,
                                             uint16_t DevAddress,
                                             uint8_t *pData,
                                             uint16_t Size)

HAL_StatusTypeDef HAL_I2C_Master_Receive_IT(I2C_HandleTypeDef *hi2c,
                                            uint16_t DevAddress,
                                            uint8_t *pData,
                                            uint16_t Size)
```

这两个函数启动传输后立即返回，完成后分别进入发送或接收回调函数：

```c
void HAL_I2C_MasterTxCpltCallback(I2C_HandleTypeDef *hi2c)
{
    if(hi2c == &hi2c1)
    {
        // 发送完成
    }
}

void HAL_I2C_MasterRxCpltCallback(I2C_HandleTypeDef *hi2c)
{
    if(hi2c == &hi2c1)
    {
        // 接收完成
    }
}
```

<mark>注意：传输结束前，数据缓冲区必须一直有效，不能使用已经退出作用域的局部数组</mark>

---

## I2C的DMA收发

```c
HAL_StatusTypeDef HAL_I2C_Master_Transmit_DMA(I2C_HandleTypeDef *hi2c,
                                              uint16_t DevAddress,
                                              uint8_t *pData,
                                              uint16_t Size)

HAL_StatusTypeDef HAL_I2C_Master_Receive_DMA(I2C_HandleTypeDef *hi2c,
                                             uint16_t DevAddress,
                                             uint8_t *pData,
                                             uint16_t Size)
```

应用示例：

```c
uint8_t sensor_data[14];
HAL_I2C_Master_Receive_DMA(&hi2c1, 0x68 << 1, sensor_data, 14);
```

DMA 传输完成后同样进入 `HAL_I2C_MasterTxCpltCallback` 或 `HAL_I2C_MasterRxCpltCallback`。使用前必须在 CubeMX 中配置对应 DMA 通道。

---

## HAL_I2C_ErrorCallback函数

函数原型：

```c
void HAL_I2C_ErrorCallback(I2C_HandleTypeDef *hi2c)
```

应用示例：

```c
volatile uint32_t i2c_error;

void HAL_I2C_ErrorCallback(I2C_HandleTypeDef *hi2c)
{
    if(hi2c == &hi2c1)
    {
        i2c_error = HAL_I2C_GetError(hi2c);
    }
}
```

常见错误包括无应答、仲裁丢失、总线错误和超时。回调函数为弱函数，需要用户自行重写。

---

## 常见问题

- **设备始终无应答**：检查 7 位地址是否正确左移、SCL/SDA 是否接反、模块是否共地以及上拉电阻是否存在。
- **总线一直忙**：检查 SDA 或 SCL 是否被外设拉低，必要时先复位从机，再重新初始化 I2C。
- **读取寄存器全为 0xFF**：检查器件供电、寄存器地址宽度、读写时序和地址表示方式。
- **EEPROM 连续写入失败**：EEPROM 写入后需要内部写周期，可使用 `HAL_I2C_IsDeviceReady` 等待器件再次应答。
- **中断或 DMA 返回 HAL_BUSY**：上一次异步传输尚未完成，不应重复启动新的传输。

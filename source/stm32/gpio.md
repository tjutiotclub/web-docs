# GPIO函数介绍

本文所列函数并非HAL库中全部GPIO相关函数，而是日常开发中最常用、最基础的操作函数。这些函数已经能够满足绝大多数GPIO的配置、读写、中断及控制需求，适用于入门学习与一般工程应用。

对于更复杂的功能（如复用功能配置、高级中断控制等），可在此基础上进一步查阅HAL库官方文档进行扩展。

---

## HAL_GPIO_Init函数

函数原型：

```c
void HAL_GPIO_Init(GPIO_TypeDef  *GPIOx, GPIO_InitTypeDef *GPIO_Init)
```

| 函数名           | HAL_GPIO_Init                                         |
| ------------- | ----------------------------------------------------- |
| 函数作用          | 根据GPIO_Init结构体中的配置参数，初始化指定的GPIO端口                     |
| 返回值           | void                                                  |
| 参数1：GPIOx     | 对应GPIO总线，其中x可以是A…I（根据具体芯片）。<br/>例如PH10，则输入GPIOH       |
| 参数2：GPIO_Init | 指向GPIO_InitTypeDef结构体的指针，该结构体包含GPIO的配置参数（如模式、速度、上下拉等） |

应用示例：

```c
GPIO_InitTypeDef GPIO_InitStruct = {0};  

GPIO_InitStruct.Pin = GPIO_PIN_10;  
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  
GPIO_InitStruct.Pull = GPIO_NOPULL;  
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;  

HAL_GPIO_Init(GPIOA, &GPIO_InitStruct); // 初始化PA10为推挽输出模式

```

---

## HAL_GPIO_ReadPin函数

函数原型：

```c
GPIO_PinState HAL_GPIO_ReadPin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);
```

| 函数名          | HAL_GPIO_ReadPin                                |
| ------------ | ----------------------------------------------- |
| 函数作用         | 读取对应的引脚当前电平状态                                   |
| 返回值          | GPIO_PinState：GPIO_PIN_SET高电平，GPIO_PIN_RESET低电平 |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I。<br/>例如PH10，则输入GPIOH         |
| 参数2：GPIO_Pin | 对应引脚数。可以是0-15。<br/>例如PH10，则输入GPIO_PIN_10        |

应用示例：

```c
HAL_GPIO_ReadPin(GPIOA,GPIO_PIN_10)//读取PA10引脚的电平状态
```

<mark>注意：该函数只读取输入寄存器状态，未初始化为输入模式时结果可能不符合预期</mark>

---

## HAL_GPIO_WritePin函数

函数原型：

```c
void HAL_GPIO_WritePin(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState)
```

| 函数名          | HAL_GPIO_WritePin                           |
| ------------ | ------------------------------------------- |
| 函数作用         | 使得对应的引脚输出高电平或者低电平                           |
| 返回值          | void                                        |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I。<br/>例如PH10，则输入GPIOH     |
| 参数2：GPIO_Pin | 对应引脚数。可以是0-15。<br/>例如PH10，则输入GPIO_PIN_10    |
| 参数3：PinState | GPIO_PIN_RESET：输出低电平<br/>GPIO_PIN_SET：输出高电平 |

应用示例：

```c
HAL_GPIO_WritePin(GPIOA,GPIO_PIN_10,GPIO_PIN_SET)//设置PA10引脚为高电平输出
```

***

## HAL_GPIO_TogglePin函数

函数原型：

```c
void HAL_GPIO_TogglePin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);
```

| 函数名          | HAL_GPIO_TogglePin                       |
| ------------ | ---------------------------------------- |
| 函数作用         | 翻转对应的引脚输出的电平                             |
| 返回值          | void                                     |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I。<br/>例如PH10，则输入GPIOH  |
| 参数2：GPIO_Pin | 对应引脚数。可以是0-15。<br/>例如PH10，则输入GPIO_PIN_10 |

应用示例：

```c
HAL_GPIO_TogglePin(GPIOA,GPIO_PIN_10)//翻转PA10引脚输出的电平状态
```

<mark>注意：仅对输出模式引脚有效</mark>

***

## HAL_GPIO_EXTI_Callback函数

函数原型：

```c
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin);
```

| 函数名          | HAL_GPIO_EXTI_Callback   |
| ------------ | ------------------------ |
| 函数作用         | 外部中断回调函数                 |
| 返回值          | void                     |
| 参数1：GPIO_Pin | 触发中断的引脚，不需要用户输入参数，程序自动传入 |

应用示例：

```c
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if(GPIO_Pin == GPIO_PIN_10)//判断是否是期望引脚触发中断
    {
    //TODO
    }
}
```

<mark>注意：该函数为弱函数，需要用户自行重写</mark>

---

## HAL_GPIO_DeInit函数

函数原型：

```c
void HAL_GPIO_DeInit(GPIO_TypeDef  *GPIOx, uint32_t GPIO_Pin)
```

| 函数名          | HAL_GPIO_DeInit                                 |
| ------------ | ----------------------------------------------- |
| 函数作用         | 将指定GPIO引脚恢复为默认复位状态（取消配置，回到上电初始状态）               |
| 返回值          | void                                            |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I（根据具体芯片）。<br/>例如PH10，则输入GPIOH |
| 参数2：GPIO_Pin | 指定要复位的引脚号，可以是GPIO_PIN_0 ~ GPIO_PIN_15           |

应用示例：

```c
HAL_GPIO_DeInit(GPIOA, GPIO_PIN_10); // 将PA10引脚恢复为默认状态
```

---

## HAL_GPIO_LockPin函数

函数原型：

```c
HAL_StatusTypeDef HAL_GPIO_LockPin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
```

| 函数名          | HAL_GPIO_LockPin                                |
| ------------ | ----------------------------------------------- |
| 函数作用         | 锁定指定GPIO引脚的配置，使其在复位前无法被再次修改（配置冻结）               |
| 返回值          | HAL_StatusTypeDef（返回操作状态，如HAL_OK表示成功）           |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I（根据具体芯片）。<br/>例如PH10，则输入GPIOH |
| 参数2：GPIO_Pin | 指定要锁定的引脚，可以是GPIO_PIN_0 ~ GPIO_PIN_15的任意组合       |

应用示例：

```c
HAL_GPIO_LockPin(GPIOA, GPIO_PIN_10); // 锁定PA10引脚配置，之后无法再修改（直到复位）
```

# GPIO函数介绍

HAL_GPIO_WritePin函数

函数原型：

```
void HAL_GPIO_WritePin(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState)
```

| 函数名          | HAL_GPIO_WritePin                                        |
| --------------- | -------------------------------------------------------- |
| 函数作用        | 使得对应的引脚输出高电平或者低电平                       |
| 返回值          | void                                                     |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I。<br/>例如PH10，则输入GPIOH |
| 参数2：GPIO_Pin | 对应引脚数。可以是0-15。<br/>例如PH10，则输入GPIO_PIN_10 |
| 参数3：PinState | GPIO_PIN_RESET：输出低电平<br/>GPIO_PIN_SET：输出高电平  |

应用示例：

```
HAL_GPIO_WritePin(GPIOA,GPIO_PIN10,GPIO_PIN_SET)
//设置PA10引脚为高电平输出
```

***

HAL_GPIO_TogglePin()

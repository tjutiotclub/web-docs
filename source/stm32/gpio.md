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
HAL_GPIO_WritePin(GPIOA,GPIO_PIN10,GPIO_PIN_SET)//设置PA10引脚为高电平输出
```

***

HAL_GPIO_ReadPin函数

函数原型：

```
GPIO_PinState HAL_GPIO_ReadPin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);
```

| 函数名          | HAL_GPIO_ReadPin                                         |
| --------------- | -------------------------------------------------------- |
| 函数作用        | 读取对应的引脚当前电平状态                               |
| 返回值          | GPIO_PinState：GPIO_PIN_SET高电平，GPIO_PIN_RESET低电平  |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I。<br/>例如PH10，则输入GPIOH |
| 参数2：GPIO_Pin | 对应引脚数。可以是0-15。<br/>例如PH10，则输入GPIO_PIN_10 |

应用示例：

```
HAL_GPIO_ReadPin(GPIOA,GPIO_PIN10,GPIO_PIN_SET)//读取PA10引脚的电平状态
```

***

HAL_GPIO_TogglePin函数

函数原型：

```
void HAL_GPIO_TogglePin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);
```

| 函数名          | HAL_GPIO_TogglePin                                       |
| --------------- | -------------------------------------------------------- |
| 函数作用        | 翻转对应的引脚输出的电平                                 |
| 返回值          | void                                                     |
| 参数1：GPIOx    | 对应GPIO总线，其中x可以是A…I。<br/>例如PH10，则输入GPIOH |
| 参数2：GPIO_Pin | 对应引脚数。可以是0-15。<br/>例如PH10，则输入GPIO_PIN_10 |

应用示例：

```
HAL_GPIO_TogglePin(GPIOA,GPIO_PIN10,GPIO_PIN_SET)//翻转PA10引脚输出的电平状态
```

***

HAL_GPIO_EXTI_Callback函数

函数原型：

```
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin);
```

| 函数名          | HAL_GPIO_EXTI_Callback                           |
| --------------- | ------------------------------------------------ |
| 函数作用        | 外部中断回调函数                                 |
| 返回值          | void                                             |
| 参数1：GPIO_Pin | 触发中断的引脚，不需要用户输入参数，程序自动传入 |

应用示例：

```
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	if(GPIO_Pin == GPIO_PIN_10)//判断是否是期望引脚触发中断
	{
	//TODO
	}
}
```


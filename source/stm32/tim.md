# TIM函数介绍

HAL_TIM_PeriodElapsedCallback函数

函数原型：

```
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim);
```

| 函数名       | HAL_TIM_PeriodElapsedCallback      |
| ------------ | ---------------------------------- |
| 函数作用     | 定时器周期性中断回调函数           |
| 返回值       | void                               |
| 参数1：*htim | 触发中断的定时器指针，无需用户输入 |

应用实例：

```
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
	if(htim == &htim1)//判断是哪个定时器触发
	{
		//TODO:定时器1中断触发执行的内容
	}

}
```


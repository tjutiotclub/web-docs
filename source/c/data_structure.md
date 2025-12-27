# 数据类型基础 —— struct 与 enum

在程序中，控制结构决定了**程序如何执行**，  
而数据结构决定了**程序操作的对象长什么样**。

在工程实践中，最重要、最常用的两种复合类型是：
- 结构体（struct）
- 枚举（enum）

它们是连接“抽象逻辑”与“真实系统状态”的关键工具。

---

## 为什么需要结构体与枚举

在真实系统中，数据往往具有以下特点：

- 不止一个变量
- 不同数据之间存在明确关联
- 数据具有“状态”或“类型”含义

如果仅使用基础类型（int、float），程序会迅速变得难以维护。

---

## 结构体（struct）

### 基本定义形式

```c
struct SensorData
{
    int16_t temperature;
    int16_t humidity;
};
````

结构体用于将**多个相关变量打包成一个整体**。

---

### 结构体的工程意义

| 特性   | 工程含义            |
| ---- | --------------- |
| 数据聚合 | 表达一个“实体”或“模块状态” |
| 可读性  | 明确字段语义，减少魔法变量   |
| 可扩展性 | 方便后期添加成员        |
| 接口清晰 | 作为函数参数/返回值更直观   |

---

## 结构体的嵌套（套用）

结构体可以作为另一个结构体的成员，这被称为**结构体嵌套**。

```c
struct IMUData
{
    float ax;
    float ay;
    float az;
};

struct RobotState
{
    struct IMUData imu;
    int16_t battery_mv;
};
```

### 工程语义

结构体嵌套表达的是：

> **“系统是由多个子模块组成的”**

这在以下场景中极其常见：

* 设备状态描述
* 通信数据帧
* 控制系统内部状态

---

## 枚举（enum）

### 基本定义形式

```c
typedef enum
{
    STATE_IDLE = 0,
    STATE_RUN,
    STATE_ERROR
} SystemState;
```

枚举用于定义**一组具有明确语义的离散值**。

---

### 枚举的工程意义

| 特性   | 工程含义            |
| ---- | --------------- |
| 可读性  | 避免使用无意义的数字常量    |
| 状态表达 | 描述系统所处状态        |
| 逻辑清晰 | 方便与 switch 结构结合 |
| 约束性  | 限定变量取值范围        |

---

## 枚举与 switch 的混合使用

这是工程 C 中**极其重要的一种组合模式**。

```c
SystemState state = STATE_IDLE;

switch (state)
{
    case STATE_IDLE:
        idle_task();
        break;

    case STATE_RUN:
        run_task();
        break;

    case STATE_ERROR:
        error_handler();
        break;

    default:
        break;
}
```

### 工程语义

该结构本质上是：

> **“基于状态的行为分发器”**

它是状态机的最小实现形式。

---

## struct + enum 的组合模式

在实际工程中，结构体和枚举通常组合使用：

```c
typedef struct
{
    SystemState state;
    int16_t speed;
    int16_t voltage;
} MotorStatus;
```

该结构表示：

* 状态是什么（enum）
* 状态相关的数据有哪些（struct）

---

## 与系统设计的关系

在嵌入式、控制系统中：

* `struct` 用于描述模块、设备、消息
* `enum` 用于描述状态、模式、命令
* `switch` 用于分发行为
* `while` 构成执行框架

它们组合起来，就形成了最基础的系统逻辑骨架。

---

## 常见工程误区

1. 用 `int` 代替 enum，语义缺失
2. 结构体字段命名随意，破坏可读性
3. 将无关数据强行塞进同一结构体
4. 枚举值与 switch 分支不一致

---

## 小结

* `struct` 的本质是：**对现实对象的结构化建模**
* `enum` 的本质是：**对离散状态的语义约束**
* `switch + enum` 是最小状态机
* `struct + enum` 是系统建模的基础

理解并正确使用它们，意味着你已经从“写语句”进入了“构建系统”的阶段。

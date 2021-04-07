# 系统文档

## 数据库设计

### 设备Device

设备名称不能重复

```json
{
    // 数据库自动生成主键
    "id": 1,
    // 设备名称
    "name": "大棚内部温度传感器",
    // 设备编号
    "dcode": "#1",
    // 设备权限 public|private
    "secret": "public",
    // 设备类型
    "type": "温度传感器",
    // 设备IP
    "ip": "192.168.1.101",
    // 端口
    "port": 8081,
    // 备注
    "description": ""
}
```

### 连接Connection

```json
{
    // 数据库自动生成主键
    "id": 1,
    // 设备ID
    "deviceId": 1,
    // 订阅的topic
    "topic": "temperature"
}
```

### 规则Rule

```json
{
    "id": 1,
    // 规则名称
    "name": "温度报警规则",
    // 规则描述
    "description": "温度超出限制报警",
    // 设备ID
    "deviceId": 1,
    // 设备topic
    "topic": "temperature",
    // 转发列
    "columns": "value,time",
    // 转发条件
    "condition": "value > 20",
    // 转发路径
    "path": "/warning/high_temperature",
    // 状态：打开-1/关闭-0。默认为0
    "status": 0
}
```

### 状态数据Status

```json
{
    "id": 1,
    // 产生数据的设备ID
    "deviceId": 1,
    // 数据值
    "value": 20.12,
    "time": // 数据格式为时间戳
}
```



## API

### 新增设备

#### Request

```json
// [POST] /device/
{
    "name": "",
    "dcode": "",
    "secret": "",
    "type": "",
    "ip": "192.168.1.101",
    "port": 8081,
    "topic": "temperature",
    "description": ""
}
```

#### Response

```json
{
    "status": 1,
    "msg": "添加成功"
}
```

### 获取设备列表

#### Request

```json
// [GET] /device/
```

#### Response

```json
[{
    "id": 1,
    "name": "大棚内部#1",
    "dcode": "",
    "secret": "",
    "type": "温度传感器",
    "ip": "192.168.1.101",
    "port": 8081,
    "status": "已连接",
    "description": ""
}]
```

### 获取设备的连接列表

#### Request

```json
// [GET] /connection/{deviceId}
```

#### Response

```json
[{
    "id": 1,
    "deviceId": 1,
    "topic": "temperature"
}]
```

### 新增规则

新增规则时后端将状态设置为1（启用）

#### Request

```json
// [POST] /rule/
{
    "name": "温度报警规则",
    "description": "温度超出限制报警",
    // 设备ID通过获取设备列表后选择获得
    "deviceId": 1,
    // topic同样
    "topic": "temperature",
    "columns": "value,time",
    "condition": "value > 20",
    "path": "",
}
```

#### Response

```json
{
    "status": 1,
    "msg": "添加成功"
}
```

### 切换规则状态

#### Request

```json
// [POST] /rule/switch/{ruleId}
```

#### Response

```json
{
    "status": 1,
    "msg": "切换成功"
}
```

### 获取规则列表

#### Request

```json
// [GET] /rule/
```

#### Response

```json
[{
    "id": 1,
    "name": "温度报警规则",
    "description": "温度超出限制报警",
    "deviceId": 1,
    "topic": "temperature",
    "columns": "value,time",
    "condition": "value > 20",
    "path": "",
    "status": 1
}]
```

### 转发处理目的地址

此接口由后端规则引擎实现转发，与前端无关

#### Request

```json
// [POST] 转发至不同的接口
{
    "ruleId": 1,
    "deviceId": 1,
    "data": {
        // 数据负载
    }
}
```

## 底层API

### 查询设备状态

device包中提供了`query_status`方法，根据设备名查询设备是否连接

### 规则引擎

后端启动时创建`RuleEngine`实例

新增设备后必须调用其`add_client`方法，参数是新增的设备实体

创建规则、修改规则后必须调用其`update_client`方法，参数是设备ID

## 数据分析设计

### 设备实时数据展示

将设备按设备类型分类，分别绘制柱状图

#### 前端：

用下拉列表选择设备类型（前端写死？跟添加设备时填的那个保持一致），或者平铺展示

纵轴是数据值，横轴是具体设备名称

每隔一段时间（5s？10s？）自动刷新一下（可选：右上角显示最后刷新时间）

#### 接口：

```json
// [GET] /api/status/realtime/<device_type>
```

返回的字典里键即为横坐标label，值为纵坐标，前端负责将返回数据格式处理成图表需要的形式

```json
{
    "东北角温度传感器": 23.12,
    "西南角温度传感器": 22.85,
    "东南角温度传感器": 24.63,
    // ……
    "平均": 23.46 // 后端负责计算并返回这一项
}
```

#### 后端：

新开一个模型（数据库表）状态数据Status（参见第一节）

上面的接口逻辑：

1. 从设备表中获取设备类型下的所有设备ID
2. 根据设备ID在数据库中查询时间戳最近的值
3. 处理数据（调整格式、计算均值）并返回

实现一个接口用于设备状态的存储：

```json
// [POST] /api/status
// POST的数据格式参见API一节 转发处理目的地址
// value和time都在请求数据的"data"里
// 返回个"{}"
```

### 设备数据变化趋势

查看某一类设备的数据变化趋势，绘制折线图

#### 前端：

用下拉列表选择设备类型，或者平铺展示

纵轴是数据值，横轴是时间，多条折线表示不同的设备（和平均值）

（可选功能：时间间隔可调整1min/5min……）

不用自动刷新

#### 接口：

```json
// [GET] /api/status/history/<device_type>
```

返回的数据里有一项`time`给出里横坐标的时间戳，其余为要显示的数据

```json
{
    "time": [],
    "东北角温度传感器": [],
    // ...
    "平均": []
}
```

#### 后端：

接口实现逻辑：

1. 从设备表中获取设备类型下的所有设备ID
2. 根据设备ID获取表中所有历史记录
3. 将记录按固定的时间间隔划分，并计算平均值，用时间间隔结束的时间戳作为横坐标值。例如计算`time`在`[a,a+d]`内的`value`的平均值，作为`a+d`时刻的数据值
4. 返回时保证各个列表的长度相同


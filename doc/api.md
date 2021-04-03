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
    // 状态：打开-1/关闭-0
    "status": 0
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


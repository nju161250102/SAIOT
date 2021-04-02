# 系统文档

## 数据库设计

### 设备Device

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
    "condition": "value > 20"
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
    "condition": "value > 20"
}
```

#### Response

```json
{
    "status": 1,
    "msg": "添加成功"
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
    "condition": "value > 20"
}]
```




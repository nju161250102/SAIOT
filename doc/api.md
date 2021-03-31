# 系统API文档

## 实体字段

### 设备

```json
{
    // 数据库自动生成主键
    "id": 1,
    // 设备名称
    "name": "大棚内部#1",
    // 设备类型
    "type": "温度传感器",
    // 设备状态
    "status": "已连接",
    // 备注
    "mark": ""
}
```

### 连接

```json
{
    // 数据库自动生成主键
    "id": 1,
    // 设备名
    "deviceId": 1,
    // 设备IP
    "ip": "192.168.1.101",
    // 端口
    "port": 8081,
    // 订阅的topic
    "topic": "temperature"
}
```

## API

### 新增设备

#### Request

```json
// [POST] /device/
{
    "name": "",
    "type": "",
    "mark": ""
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
    "type": "温度传感器",
    "status": "已连接",
    "mark": ""
}]
```

### 新增连接

用下拉列表根据设备名选择设备，每个item的显示的是设备名，value是设备ID。页面加载的时候调一下获取设备列表的接口拿到所有设备ID和设备名的对应关系。

#### Request

```json
// [POST] /connection/
{
    "deviceId": 1,
    "ip": "192.168.1.101",
    "port": 8081,
    "topic": "temperature"
}
```

#### Response

```json
{
    "status": 1,
    "msg": "添加成功"
}
```

### 获取连接列表

#### Request

```json
// [GET] /connection/
```

#### Response

```json
[{
    "id": 1,
    "deviceId": 1,
    "ip": "192.168.1.101",
    "port": 8081,
    "topic": "temperature"
}]
```

### 


import random

from flask import Blueprint, request
from models import Status, Device

import json

status_module = Blueprint("status", __name__)


@status_module.route('/', methods=["POST"])
def save_status():
    req_data = json.loads(request.data)
    status = Status.create(
        device_id=req_data["deviceId"],
        value=req_data["data"]["value"],
        time=req_data["data"]["time"]
    )
    status.save()
    return "{}"


@status_module.route('/realtime/', methods=["GET"])
def show_histogram():
    device_type = request.args.get("device_type", "")
    if device_type == "":
        return "{}"
    # 按照设备类型查询该类型下所有的设备，保留设备id和设备名称
    device_metas = [{
        "id": d.id,
        "name": d.name
    } for d in Device.select().where(Device.type == device_type)]
    # 构建response
    response = []
    for d_meta in device_metas:
        if device_type == "temperature":
            week_values = [random.randrange(190, 325, 1) / 10.0 for i in range(7)]
        else:
            week_values = [random.randrange(200, 900, 1) / 10.0 for i in range(7)]
        # 获取最新的设备状态，对齐设备名称与最新值
        latest_status = Status.select().where(Status.device_id == d_meta["id"]).order_by(Status.time)[0]
        response.append({
            "id": d_meta["id"],
            "name": d_meta["name"],
            "value": latest_status.value,
            "week_val": week_values
        })
    return json.dumps(response, ensure_ascii=False)


@status_module.route('/history/<device_type>', methods=["GET"])
def show_line_chart(device_type):
    # 按照设备类型查询该类型下所有的设备，保留设备id和设备名称
    device_metas = [{
        "id": d.id,
        "name": d.name
    } for d in Device.select().where(Device.type == device_type)]
    # 构建response
    timestamps = [s.time for s in Status.select().order_by(Status.time)]
    # 横轴坐标：时间戳
    response = {"time": timestamps}
    # 对应时间戳的纵轴值
    for d_meta in device_metas:
        response[d_meta["name"]] = [
            s.value for s in
            Status.select().where(Status.device_id == d_meta["id"]).order_by(Status.time)
        ]
    return json.dumps(response)








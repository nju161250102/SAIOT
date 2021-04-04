from flask import Blueprint, request
from models import Device
import json

device_module = Blueprint("device", __name__)


@device_module.route('/', methods=["POST"])
def add_device():
    # Attributes can be null
    name = request.form['name']
    dcode = request.form['dcode']
    secret = request.form['secret']
    device_type = request.form['type']
    description = request.form['description']
    # Attributes cannot be null
    ip = request.form['ip']
    port = request.form['port']
    topic = request.form['topic']
    # Set response if error.
    # err_msg = '添加设备失败：'
    # is_error = False
    # if ip is None:
    #     err_msg += '设备ip不能为空！'
    #     is_error = True
    # if port is None:
    #     err_msg += '设备port不能为空！'
    #     is_error = True
    # if topic is None:
    #     err_msg += '设备topic不能为空！'
    #     is_error = True
    # if is_error:
    #     response = {'status': 0, 'msg': err_msg}
    #     return json.dumps(response, ensure_ascii=False)

    # Query db and set response if success.
    device = Device.create(
        name=name, dcode=dcode, secret=secret, type=device_type,
        ip=ip, port=port, topic=topic, description=description
    )
    device.save()
    response = {'status': 1, 'msg': "添加成功"}
    return json.dumps(response, ensure_ascii=False)


@device_module.route('/', methods=["GET"])
def get_all_device():
    devices = Device.select()
    return json.dumps(devices)

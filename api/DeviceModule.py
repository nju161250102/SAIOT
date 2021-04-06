from flask import Blueprint, request
from models import Device, Connection
from rule import RuleEngine
from device import query_status

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
    device = Device.create(
        name=name, dcode=dcode, secret=secret, type=device_type,
        ip=ip, port=port, description=description
    )
    device.save()
    for s in topic.split(";"):
        Connection.create(device_id=device.id, topic=s.strip()).save()
    RuleEngine.add_client(device)
    response = {'status': 1, 'msg': "添加成功"}
    return json.dumps(response, ensure_ascii=False)


@device_module.route('/', methods=["GET"])
def get_all_device():
    result = []
    for device in Device.select():
        topics = [c.topic for c in Connection.select().where(Connection.device_id == device.id)]
        result.append({
            "id": device.id,
            "name": device.name,
            "dcode": device.dcode,
            "secret": device.secret,
            "type": device.type,
            "description": device.description,
            "ip": device.ip,
            "port": device.port,
            "topic": ",".join(topics),
            "status": 1 if query_status(device.name) else 0
        })
    return json.dumps(result)

from flask import Blueprint
from models import Connection
import json


connection_module = Blueprint("/connection", __name__)


@connection_module.route("/<device_id>", methods=["GET"])
def get_connection_list_for_device(device_id):
    result = [{
        "id": c.id,
        "deviceId": c.device_id,
        "topic": c.topic
    } for c in Connection.select().where(Connection.device_id == int(device_id))]
    return json.dumps(result, ensure_ascii=False)

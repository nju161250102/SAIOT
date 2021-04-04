from flask import Blueprint, request
from models import Connection
import json


connection_module = Blueprint("/connection", __name__)


@connection_module.route("/<device_id>", methods=["GET"])
def get_connection_list_for_device(device_id):
    connections = Connection.select().where(Connection.device_id == int(device_id))
    return json.dumps(connections, ensure_ascii=False)

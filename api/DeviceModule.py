from flask import Blueprint

device_module = Blueprint("device", __name__)


@device_module.route('/', methods=["POST"])
def add_device():
    pass


@device_module.route('/', methods=["GET"])
def get_all_device():
    pass

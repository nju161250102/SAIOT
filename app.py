import logging
from flask import Flask, render_template
from flask_cors import CORS

from models import Device
from rule import RuleEngine
from api import device_module, rule_module, connection_module, status_module
from config import host

app = Flask(__name__)
app.register_blueprint(device_module, url_prefix='/api/device/')
app.register_blueprint(rule_module, url_prefix='/api/rule/')
app.register_blueprint(connection_module, url_prefix='/api/connection/')
app.register_blueprint(status_module, url_prefix='/api/status/')
CORS(app, supports_credentials=True)


@app.route('/')
def index_page():
    return render_template('index.html')


if __name__ == '__main__':
    formatter = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    RuleEngine.init(Device.select())
    app.run(host=host)

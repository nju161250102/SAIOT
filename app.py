from flask import Flask, render_template
from api import device_module, rule_module

app = Flask(__name__)
app.register_blueprint(device_module, url_prefix='/api/device/')
app.register_blueprint(rule_module, url_prefix='/api/rule/')


@app.route('/')
def index_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

from flask import Blueprint, request
from models import Rule
import json


rule_module = Blueprint("rule", __name__)


@rule_module.route('/', methods=['POST'])
def add_rule():
    # Draw attributes from form.
    name = request.form['name']
    description = request.form['description']
    device_id = request.form['deviceId']
    temperature = request.form['temperature']
    columns = request.form['columns']
    condition = request.form['condition']
    path = request.form['path']
    # Query db and set response if success.
    rule = Rule.create(
        name=name, description=description, device_id=device_id,
        temperature=temperature, columns=columns,
        condition=condition, path=path
    )
    rule.save()
    response = {"status": 1, "msg": "添加成功"}
    return json.dumps(response, ensure_ascii=False)


@rule_module.route('/', methods=['GET'])
def get_all_rule():
    rules = Rule.select()
    return json.dumps(rules, ensure_ascii=False)


@rule_module.route('/switch/<rule_id>', methods=['POST'])
def switch_rule(rule_id):
    rule = Rule.select().where(Rule.id == int(rule_id))
    ori_status = int(rule.status)
    new_status = (ori_status + 1) % 2
    # Update: Switch status from 1 -> 0 or 0 -> 1
    rule.status = new_status
    msg = "将规则%s的状态从%s切换至%s" % (rule_id, ori_status, new_status)
    response = {"status": 1, "msg": msg}
    return json.dumps(response, ensure_ascii=False)

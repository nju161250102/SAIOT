import asyncio
import json
import logging
from threading import Thread

import requests
from hbmqtt.client import MQTTClient, ClientException
from requests import RequestException

from .RuleParser import RuleParser
from models import Rule
from config import host


class Client(Thread):

    def __init__(self, device):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = MQTTClient(loop=self.loop)
        self.name = device.name
        self.device_id = device.id
        self.version = 0
        self.rules = Rule.select().where(Rule.device_id == self.device_id and Rule.status == 1)
        logging.info("Device %s loads %d rules" % (self.name, len(self.rules)))

    def run(self) -> None:
        try:
            self.loop.run_until_complete(self.connect())
            self.loop.run_until_complete(self.subscribe())
            while True:
                current_version = self.version
                while current_version == self.version:
                    self.loop.run_until_complete(self.handle())
                self.rules = Rule.select().where(Rule.device_id == self.device_id and Rule.status == 1)
                logging.info("Device %s loads %d rules" % (self.name, len(self.rules)))
        finally:
            logging.error("Load rule failed: " + self.name)
            self.loop.close()

    async def connect(self):
        await self.client.connect('ws://127.0.0.1:8081/')

    async def subscribe(self):
        await self.client.subscribe([(self.name + "/" + r.topic, 0x02) for r in self.rules])

    async def handle(self):
        try:
            message = await self.client.deliver_message()
            packet = message.publish_packet
            for r in self.rules:
                if packet.variable_header.topic_name == self.name + "/" + r.topic:
                    data = json.loads(packet.payload.data.decode(encoding="utf-8"))
                    # 如果规则匹配
                    if RuleParser(r.condition).evaluate(data):
                        logging.info("Rule: %d, %s => %s" %
                                     (r.id, packet.variable_header.topic_name, packet.payload.data.decode(encoding="utf-8")))
                        forward_data = dict(filter(lambda s: s[0] in r.columns.strip(","), data.items()))
                        try:
                            requests.post("http://%s:5000/%s" % (host, r.path), data=json.dumps({
                                "ruleId": r.id,
                                "deviceId": self.device_id,
                                "data": forward_data
                            }))
                        except RequestException as e:
                            break
        except ClientException as ce:
            logging.error("Client exception: %s" % ce)
            await self.client.unsubscribe([(self.name + "/" + r.topic, 0x02) for r in self.rules])
            await self.client.disconnect()

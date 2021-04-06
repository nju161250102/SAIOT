import asyncio
import json
import logging
from threading import Thread

import requests
from hbmqtt.client import MQTTClient, ClientException

from .RuleParser import RuleParser


class Client(Thread):

    def __init__(self, device_name):
        super().__init__()
        self.client = MQTTClient()
        self.name = device_name
        self.loop = asyncio.get_event_loop()
        self.version = 0
        self.rules = []

    def run(self) -> None:
        self.loop.run_until_complete(self.connect())
        self.loop.run_until_complete(self.subscribe())
        while True:
            # TODO 根据设备ID从数据库中获取启用的规则列表
            logging.info("Device %s loads %d rules" % (self.name, len(self.rules)))
            current_version = self.version
            while current_version == self.version:
                self.loop.run_until_complete(self.handle())

    async def connect(self):
        await self.client.connect('ws://127.0.0.1:8081/')

    async def subscribe(self):
        await self.client.subscribe([(self.name + "/" + r.topic, 0x02) for r in self.rules])

    async def handle(self):
        try:
            message = await self.client.deliver_message()
            packet = message.publish_packet
            for r in self.rules:
                if packet.variable_header.topic_name == r.topic:
                    data = json.loads(packet.payload.data.decode(encoding="utf-8"))
                    # 如果规则匹配
                    if RuleParser(r.condition).evaluate(data):
                        forward_data = dict(filter(lambda s: s[0] in r.columns, data))
                        requests.post("http://127.0.0.1:8080/" + r.path, data=json.dumps(forward_data))
        except ClientException as ce:
            logging.error("Client exception: %s" % ce)
            await self.client.unsubscribe([(self.name + "/" + r.topic, 0x02) for r in self.rules])
            await self.client.disconnect()

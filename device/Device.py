import logging
import asyncio

from hbmqtt.client import MQTTClient, ConnectException


class Device:

    def __init__(self, name, topic, g, interval: int):
        self.client = MQTTClient()
        self.name = name
        self.topic = topic
        self.g = g
        self.interval = interval

    async def publish(self):
        code = await self.client.connect('ws://127.0.0.1:8081/')
        if code == 0:
            logging.info("%s connected" % self.name)
        else:
            logging.error("%s failed" % self.name)
        try:
            while True:
                try:
                    await self.client.publish(self.topic, bytearray(str(next(self.g)), 'utf-8'), qos=0x02)
                    await asyncio.sleep(self.interval)
                except StopIteration:
                    break
            await self.client.disconnect()
        except ConnectException as ce:
            logging.error("Connection failed: %s" % ce)
            asyncio.get_event_loop().stop()

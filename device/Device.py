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
        self.connected = False

    async def connect(self):
        code = await self.client.connect('ws://127.0.0.1:8081/')
        if code == 0:
            self.connected = True
            logging.info("%s connected" % self.name)
        else:
            logging.error("%s failed" % self.name)

    async def publish(self):
        if self.connected:
            try:
                while True:
                    try:
                        await self.client.publish(self.topic, bytearray(str(next(self.g)), 'utf-8'), qos=0x02)
                        await asyncio.sleep(self.interval)
                    except StopIteration:
                        break
            except ConnectException as ce:
                logging.error("Connection failed: %s" % ce)
            finally:
                await self.client.disconnect()

    async def ping(self):
        try:
            while True:
                await self.client.publish("status/" + self.name, b"ok", qos=0x02)
                await asyncio.sleep(1)
        except ConnectException as ce:
            logging.error("Connection failed: %s" % ce)
        finally:
            await self.client.disconnect()

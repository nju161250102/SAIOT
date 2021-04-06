import logging
import asyncio
from hbmqtt.broker import Broker


class MyBroker:

    def __init__(self):
        config = {
            'listeners': {
                'default': {
                    'bind': '127.0.0.1:8081',
                    'type': 'ws',
                    'max_connections': 20,
                },
            },
            'sys_interval': 10,
            'auth': {
                'allow-anonymous': True,
                'plugins': [
                    'auth_anonymous'
                ]
            },
            'topic-check': {
                'enabled': True,
                'plugins': [
                    'topic_taboo'
                ]
            }
        }
        self.broker = Broker(config)

    async def test_broker(self):
        await self.broker.start()

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.test_broker())
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    MyBroker().start()

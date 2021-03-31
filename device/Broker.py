import logging
import asyncio
from hbmqtt.broker import Broker

logger = logging.getLogger(__name__)


class MyBroker:

    def __init__(self):
        config = {
            'listeners': {
                'default': {
                    'type': 'tcp',
                    'bind': '127.0.0.1:1883',
                },
                'ws-mqtt': {
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

    @asyncio.coroutine
    def test_broker(self):
        yield from self.broker.start()

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.test_broker())
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    MyBroker().start()

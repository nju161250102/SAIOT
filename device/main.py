import logging
import math
import asyncio
import random

from hbmqtt.client import MQTTClient
from device import Device


async def async_query_status(device_name: str):
    status = False
    client = MQTTClient()
    await client.connect('ws://127.0.0.1:8081/')
    await client.subscribe([
        (device_name + "/status", 0x02),
    ])
    try:
        message = await client.deliver_message(2)
        status = (message.packet_id is not None)
    except TimeoutError as ce:
        logging.error("Client exception: %s" % ce)
    finally:
        await client.unsubscribe(device_name + "/status")
        await client.disconnect()
        return status


def query_status(device_name: str):
    """
    设备状态查询接口

    :param device_name: 设备名
    :return: bool 表示是否连接
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    get_future = asyncio.ensure_future(async_query_status(device_name))
    loop.run_until_complete(get_future)
    return get_future.result()


def temperature_fun(high, low, T, interval):
    i = 0
    while True:
        y = round(math.sin(2 * math.pi / T * i) * (high - low) / 2 + (high + low) / 2 + (random.randrange(-40, 40) / 10), 2)
        yield y
        i += interval
        if i >= T:
            i = 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    # 设备列表，在此处新增设备
    device_list = [Device("东北角温度", "temperature", temperature_fun(25, 8, 120, 1), 0.5),
                   Device("东南角温度", "temperature", temperature_fun(24, 8, 120, 1), 0.5),
                   Device("西南角温度", "temperature", temperature_fun(25, 7, 120, 1), 0.5),
                   Device("西北角温度", "temperature", temperature_fun(24, 7, 120, 1), 0.5)]
    # 先建立连接
    future = asyncio.gather(*[d.connect() for d in device_list])
    asyncio.get_event_loop().run_until_complete(future)
    # 启动设备的发布和ping
    future = asyncio.gather(*[d.publish() for d in device_list], *[d.ping() for d in device_list])
    asyncio.get_event_loop().run_until_complete(future)

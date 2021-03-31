import logging
import math
import asyncio

from Device import Device


def temperature_fun(high, low, T, interval):
    i = 0
    while True:
        y = math.sin(2 * math.pi / T * i) * (high - low) / 2 + (high + low) / 2
        yield y
        i += interval
        if i >= T:
            i = 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    temperature_device = Device("温度1", "temp1", temperature_fun(22, 8, 12, 1), 2)
    device_list = []
    device_list.append(temperature_device.publish())
    future = asyncio.gather(*device_list)
    asyncio.get_event_loop().run_until_complete(future)

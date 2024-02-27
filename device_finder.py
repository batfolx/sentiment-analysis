import concurrent.futures as future
import _thread
import socket
import asyncio
import functools
import time
import datetime
import pickle


class DeviceTracker:
    def __init__(self):
        self.devices = {}
        self.record = {}

    def __str__(self):
        return str(self.record)

    def __repr__(self):
        return self.__str__()

    def update(self):
        """
        update the dictionary that keeps track of connected devices
        :return:
        """
        my_time = datetime.datetime.now()
        now = (my_time.second, my_time.minute, my_time.hour, my_time.day, my_time.month, my_time.year)
        for device in self.devices:
            self.process(device, now)

    def process(self, device: str, now: tuple):
        """
        add device and time to record
        :param device: device ID
        :param now: current time
        :return:
        """
        if device not in self.record:
            self.record[device] = [[now]]
        elif len(self.record[device][-1]) == 2:
            self.record[device].append([now])
        else:
            self.record[device][-1].append(now)



def make_async(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(fn, *args, **kwargs)
    return wrapper


def timeout(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await asyncio.wait_for(fn(*args, *kwargs), timeout=1)
        except TimeoutError:
            return tuple()
    return wrapper


@timeout
@make_async
def check_addr(ip: str) -> tuple:
    """
    check if IPv4 is findable, return valid address name
    :param ip: IPv4 address
    :return: host name and address
    """
    try:
        return socket.gethostbyaddr(ip)
    except socket.gaierror:
        return tuple()
    except socket.herror:
        return tuple()


async def find_devices(dt: DeviceTracker):
    """
    find devices on local network
    :return:
    """
    loop = asyncio.get_running_loop()
    loop.set_default_executor(future.ThreadPoolExecutor(max_workers=1000))
    addr = socket.gethostbyname(socket.gethostname())
    index = addr.rfind('.')
    base = addr[:index+1]
    args = [base + str(i) for i in range(1000)]
    tasks = [check_addr(x) for x in args]
    results = await asyncio.gather(*tasks)
    dt.devices = {x[0].lower(): x[2] for x in results if x}
    print('devices: ')
    for key in dt.devices:
        print(f'{key}: {dt.devices[key]}')
    dt.update()

    # return devices


def run_find_devices(dt: DeviceTracker):
    """
    run as thread to prevent blocking
    :param dt: object to keep track of devices
    :return:
    """
    print('running')
    asyncio.run(find_devices(dt))


if __name__ == '__main__':
    device_tracker = DeviceTracker()
    # asyncio.run(find_devices(device_tracker))
    for i in range(5):
        _thread.start_new_thread(run_find_devices, (device_tracker,))
        time.sleep(1.3)
        print(device_tracker.record)
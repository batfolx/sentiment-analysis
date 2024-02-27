import functools
import asyncio

def make_async(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(fn, *args, **kwargs)
    return wrapper


def timeout(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            async with asyncio.timeout(1):
                return await asyncio.wait_for(fn(*args, *kwargs), timeout=3)
        except TimeoutError:
            return tuple()
    return wrapper

import asyncio

from src.handlers.bitfinex_handler import BitfinexHandler


async def example_bitfinex_handler():
    handler = BitfinexHandler()
    handler.register_callback(print)
    await handler.open()
    await handler.listen()


asyncio.run(example_bitfinex_handler())

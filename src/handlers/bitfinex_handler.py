import json
from typing import Callable

import websockets
from PySide6.QtCore import Signal, QObject


class BitfinexHandler(QObject):
    PUBLIC_URL = "wss://api-pub.bitfinex.com/ws/2"
    connected = Signal()
    disconnected = Signal()

    def __init__(self):
        super().__init__()

        self.websocket = None
        self.channel_id = None
        self.callbacks = []

    def register_callback(self, callback: Callable):
        self.callbacks.append(callback)

    async def open(self):
        self.websocket = await websockets.connect(self.PUBLIC_URL)
        await self.subscribe(symbol="tBTCUSD")

    async def close(self):
        await self.unsubscribe()
        await self.websocket.close()
        self.disconnected.emit()

    async def listen(self):
        async for message in self.websocket:
            data = json.loads(message)
            if isinstance(data, dict) and data["event"] == "subscribed":
                self.channel_id = data["chanId"]
                self.connected.emit()
            elif isinstance(data, list):
                for callback in self.callbacks:
                    callback(data)

    async def subscribe(self, symbol: str):
        message = {
            "event": "subscribe",
            "channel": "book",
            "symbol": symbol
        }
        await self.websocket.send(json.dumps(message))

    async def unsubscribe(self):
        message = {
            "event": "unsubscribe",
            "chanId": self.channel_id
        }
        await self.websocket.send(json.dumps(message))

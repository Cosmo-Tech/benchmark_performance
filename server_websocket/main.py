#!/usr/bin/env python

import asyncio
import json
import websockets

USERS = set()

async def handler(websocket):
    global USERS, VALUE
    try:
        # Register user
        USERS.add(websocket)
        # Manage state changes
        async for message in websocket:
            websockets.broadcast(USERS, message)
    finally:
        # Unregister user
        USERS.remove(websocket)
        # websockets.broadcast(USERS, "")

async def main():
    async with websockets.serve(handler, "localhost", 11234):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
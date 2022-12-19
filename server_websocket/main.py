#!/usr/bin/env python

import asyncio
import json
import websockets

USERS = set()
def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def handler(websocket):
    global USERS, VALUE
    try:
        # Register user
        USERS.add(websocket)
        # websockets.broadcast(USERS, users_event())
        # Send current state to user
        # await websocket.send("Hello")
        # Manage state changes
        async for message in websocket:
            websockets.broadcast(USERS, message)
    finally:
        # Unregister user
        USERS.remove(websocket)
        # websockets.broadcast(USERS, "")

async def main():
    async with websockets.serve(handler, "localhost", 1234):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
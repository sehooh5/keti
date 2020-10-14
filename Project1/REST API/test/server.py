import asyncio
import json
import logging
import websockets
import os

logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "cam1":
                STATE["value"] -= 1
                os.environ['OPENCV_CAMERA_SOURCE'] = "rtsp://keti:keti1234@192.168.100.70:8810/videoMain"
                print(os.environ['OPENCV_CAMERA_SOURCE'])
                await notify_state()
            elif data["action"] == "cam2":
                STATE["value"] += 1
                os.environ['OPENCV_CAMERA_SOURCE'] = "rtsp://keti:keti1234@192.168.100.60:8805/videoMain"
                print(os.environ['OPENCV_CAMERA_SOURCE'])
                await notify_state()
            elif data["action"] == "cam3":
                STATE["value"] = 0
                os.environ['OPENCV_CAMERA_SOURCE'] = "rtsp://keti:keti1234@192.168.100.60:8805/videoMain"
                print(os.environ['OPENCV_CAMERA_SOURCE'])
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

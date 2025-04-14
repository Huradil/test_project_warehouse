import json
from collections import defaultdict

active_connections = defaultdict(set)


async def websocket_application(scope, receive, send):
    if scope["type"] == "websocket.connect":
        await send({"type": "websocket.accept"})

    room_name = "notifications"
    room_group_name = f"group_{room_name}"

    active_connections[room_group_name].add(send)

    while True:
        event = await receive()

        # if event["type"] == "websocket.connect":
        #     await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            active_connections[room_group_name].remove(send)
            break

        if event["type"] == "websocket.receive":
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong!"})
    active_connections[room_group_name].remove(send)


async def broadcast_message(message: str):
    for connection in active_connections["group_notifications"]:
        await connection({"type": "websocket.send", "text": json.dumps({"messages": message})})

import json
from collections import defaultdict

active_connections = defaultdict(set)


async def websocket_application(scope, receive, send):
    if scope["type"] == "websocket":
        room_name = "notifications"
        room_group_name = f"group_{room_name}"

        active_connections[room_group_name].add(send)
        try:
            await send({"type": "websocket.accept"})

            while True:
                event = await receive()

                if event["type"] == "websocket.disconnect":
                    break

                if event["type"] == "websocket.receive":
                    if event.get("text") == "ping":
                        await send({"type": "websocket.send", "text": "pong!"})
        finally:
            active_connections[room_group_name].discard(send)


async def broadcast_message(message: str):
    room_group_name = "group_notifications"
    dead_connections = set()

    for connection in active_connections[room_group_name]:
        try:
            await connection({
                "type": "websocket.send",
                "text": json.dumps({"messages": message})
            })
        except Exception as e:
            dead_connections.add(connection)

    for conn in dead_connections:
        active_connections[room_group_name].discard(conn)

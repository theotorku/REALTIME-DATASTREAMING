# server.py

import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request
from kafka import KafkaConsumer
from typing import List
from fastapi.responses import JSONResponse


app = FastAPI()

KAFKA_BROKER = "localhost:9092"
TOPIC = "polygon.stocks"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='latest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id="websocket-group"
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def sync_kafka_consume():
    for message in consumer:
        data = message.value
        asyncio.run_coroutine_threadsafe(
            manager.broadcast(data), asyncio.get_event_loop())


@app.on_event("startup")
def startup_event():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, sync_kafka_consume)

"""
FastAPI application entry point for the AI Civilization Simulator.

Milestone 0:
  - GET  /             → health check
  - GET  /api/world    → full world state as JSON
  - WS   /ws           → WebSocket skeleton (sends world state on connect)
"""

import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.world import WorldGrid

# ---------------------------------------------------------------------------
# App Setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="WorldSeed API",
    description="Backend simulation engine for the AI Civilization Simulator",
    version="0.1.0",
)

# CORS – allow the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# World Instance
# ---------------------------------------------------------------------------

world = WorldGrid(width=50, height=50)

# ---------------------------------------------------------------------------
# REST Endpoints
# ---------------------------------------------------------------------------


@app.get("/")
async def health_check():
    """Server health / version probe."""
    return {
        "status": "ok",
        "project": "WorldSeed",
        "milestone": 0,
        "world_size": f"{world.width}x{world.height}",
    }


@app.get("/api/world")
async def get_world():
    """Return the full serialized world grid."""
    return world.to_dict()


# ---------------------------------------------------------------------------
# WebSocket Hub (Skeleton)
# ---------------------------------------------------------------------------

class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint.

    Milestone 0: On connect, sends the full world state once.
    Future milestones will stream tick deltas here.
    """
    await manager.connect(websocket)
    try:
        # Send initial world state
        world_data = world.to_dict()
        await websocket.send_text(json.dumps({
            "type": "world_init",
            "payload": world_data,
        }))

        # Keep connection alive — future milestones will push tick updates
        while True:
            data = await websocket.receive_text()
            # Milestone 0: echo back any client messages as acknowledgment
            await websocket.send_text(json.dumps({
                "type": "ack",
                "payload": data,
            }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)

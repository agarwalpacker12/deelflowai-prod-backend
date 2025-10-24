"""
WebSocket endpoints for real-time updates
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
        
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket, user_id: int = None):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
        
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    async def send_to_user(self, message: str, user_id: int):
        """Send message to specific user"""
        if user_id in self.user_connections:
            for websocket in self.user_connections[user_id]:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending to user {user_id}: {e}")
    
    async def broadcast(self, message: str):
        """Broadcast message to all connections"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")

manager = ConnectionManager()

@router.websocket("/live-activity")
async def websocket_live_activity(websocket: WebSocket):
    """WebSocket endpoint for live activity feed"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            
            # Echo back for testing
            await manager.send_personal_message(f"Echo: {data}", websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/user/{user_id}")
async def websocket_user_updates(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for user-specific updates"""
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Process user-specific data
            try:
                message_data = json.loads(data)
                message_data["user_id"] = user_id
                
                # Echo back with user context
                await manager.send_personal_message(
                    json.dumps(message_data), 
                    websocket
                )
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({"error": "Invalid JSON"}), 
                    websocket
                )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

@router.websocket("/notifications")
async def websocket_notifications(websocket: WebSocket):
    """WebSocket endpoint for notifications"""
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Process notification data
            try:
                notification = json.loads(data)
                await manager.send_personal_message(
                    json.dumps({
                        "type": "notification",
                        "data": notification,
                        "timestamp": "2024-01-01T00:00:00Z"
                    }), 
                    websocket
                )
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({"error": "Invalid notification format"}), 
                    websocket
                )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Helper functions for sending updates
async def send_activity_update(activity_data: Dict[str, Any]):
    """Send activity update to all connected clients"""
    message = json.dumps({
        "type": "activity_update",
        "data": activity_data,
        "timestamp": "2024-01-01T00:00:00Z"
    })
    await manager.broadcast(message)

async def send_user_notification(user_id: int, notification_data: Dict[str, Any]):
    """Send notification to specific user"""
    message = json.dumps({
        "type": "notification",
        "data": notification_data,
        "timestamp": "2024-01-01T00:00:00Z"
    })
    await manager.send_to_user(message, user_id)

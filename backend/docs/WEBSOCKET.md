# WebSocket Implementation Guide

## Overview

This application uses Django Channels with Redis for real-time WebSocket communication. The implementation supports:

- Real-time user presence tracking
- Live updates for BucketPoints (bucketlist items)
- Live updates for Photos
- Message notifications
- Heartbeat/ping-pong for connection health monitoring

## Architecture

### Backend Components

```
core/websocket/
├── consumers.py    # WebSocket consumer (connection handling, heartbeat)
├── messages.py     # Message type enum definitions
├── utils.py        # Utility functions for broadcasting
└── routing.py      # URL routing for WebSocket connections
```

### Frontend Components

```
src/
├── services/WebSocketClient.ts       # Core WebSocket client with reconnection
├── contexts/WebSocketProvider.tsx    # React context for WebSocket
├── hooks/usePhotosWithWebSocket.ts   # Hook for real-time photo updates
├── components/ConnectionStatusIndicator.tsx  # UI for connection status
└── types/
    ├── websockets.ts                 # Message type enum
    ├── websocket-interfaces.ts       # Message payload interfaces
    └── websocket-messages.ts         # Type mapping
```

## Message Types

All supported WebSocket message types:

| Type | Description |
|------|-------------|
| `MESSAGE_CREATED` | New chat message |
| `MESSAGE_DELETED` | Chat message deleted |
| `MESSAGE_VIEWED` | Chat message viewed |
| `USER_PRESENCE_CONNECTED` | User came online |
| `USER_PRESENCE_DISCONNECTED` | User went offline |
| `BUCKETPOINT_CREATED` | New bucketlist item |
| `BUCKETPOINT_UPDATED` | Bucketlist item modified |
| `BUCKETPOINT_DELETED` | Bucketlist item removed |
| `PHOTO_UPLOADED` | New photo added |
| `PHOTO_UPDATED` | Photo metadata changed |
| `PHOTO_DELETED` | Photo removed |
| `ALBUM_CREATED` | New album created |
| `ALBUM_UPDATED` | Album metadata changed |
| `ALBUM_DELETED` | Album removed |
| `SYSTEM_NOTIFICATION` | System-wide notification |

## Configuration

### Backend

**Environment Variables:**
- `REDIS_HOST`: Redis server hostname (default: `localhost`)

**Django Settings (`settings.py`):**
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv("REDIS_HOST", "localhost"), 6379)],
        },
    },
}

ASGI_APPLICATION = "backend.asgi.application"
```

### Frontend

**Environment Variables (`.env`):**
```
REACT_APP_WS_URL=ws://127.0.0.1:8000/ws/
```

**Production:** The WebSocket URL is automatically constructed from the current origin.

### Nginx Configuration

For production, ensure nginx proxies WebSocket connections:

```nginx
location /ws/ {
    proxy_pass http://backend/ws/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_read_timeout 86400;  # 24 hours keep-alive
}
```

## Authentication

WebSocket connections are authenticated via JWT token passed as a query parameter:

```
ws://host/ws/?accessToken=<jwt_token>
```

The backend validates the token using Django's `SECRET_KEY` and retrieves the user from the database.

**Connection rejection codes:**
- `4001`: Unauthenticated (missing or invalid token)
- `4000`: Server error during connection

## Features

### Heartbeat/Ping-Pong

The server sends `PING` messages every 30 seconds. The client responds with `PONG` to confirm the connection is alive.

**Configuration (backend):**
```python
HEARTBEAT_INTERVAL = 30  # seconds
HEARTBEAT_TIMEOUT = 10   # seconds
MAX_MESSAGE_SIZE = 65536 # 64KB
```

### Reconnection (Frontend)

The client automatically reconnects with exponential backoff:

- Initial delay: 1 second
- Maximum delay: 30 seconds
- Multiplier: 1.5x
- Maximum attempts: 20

### Message Queue

Messages are queued when disconnected and sent upon reconnection:

- Maximum queue size: 100 messages
- Maximum message age: 60 seconds

## Usage

### Backend: Broadcasting Messages

```python
from core.websocket.utils import send_ws_message_to_user, broadcast_ws_message
from core.websocket.messages import WebSocketMessageType

# Send to single user
send_ws_message_to_user(
    user_id=1,
    event_type=WebSocketMessageType.PHOTO_UPLOADED,
    data={"data": photo_data, "album_id": album_id}
)

# Broadcast to multiple users
broadcast_ws_message(
    user_ids=[1, 2, 3],
    event_type=WebSocketMessageType.BUCKETPOINT_CREATED,
    data={"data": bucketpoint_data}
)
```

### Frontend: Subscribing to Events

```typescript
import { useWebSocketContext } from "../contexts/WebSocketProvider"
import { WebSocketMessageType } from "../types/websockets"

function MyComponent() {
    const websocket = useWebSocketContext()

    useEffect(() => {
        const handlePhotoUploaded = (data: PhotoUploaded) => {
            console.log("New photo:", data)
        }

        websocket.bind(WebSocketMessageType.PhotoUploaded, handlePhotoUploaded)

        return () => {
            websocket.unbind(WebSocketMessageType.PhotoUploaded, handlePhotoUploaded)
        }
    }, [websocket])

    return <div>...</div>
}
```

### Frontend: Connection Status

```typescript
import ConnectionStatusIndicator from "../components/ConnectionStatusIndicator"

function Header() {
    return (
        <header>
            <ConnectionStatusIndicator showLabel={true} />
        </header>
    )
}
```

### Frontend: Real-time Photos Hook

```typescript
import { usePhotosWithWebSocket } from "../hooks/usePhotosWithWebSocket"

function PhotoGallery({ albumId }: { albumId: string }) {
    const { photos, isLoading, isError, refetch } = usePhotosWithWebSocket(albumId)

    if (isLoading) return <Loading />
    if (isError) return <Error />

    return (
        <div>
            {photos.map(photo => <PhotoCard key={photo.id} photo={photo} />)}
        </div>
    )
}
```

## Troubleshooting

### Connection Issues

1. **Check Redis is running:**
   ```bash
   redis-cli ping
   ```

2. **Check WebSocket endpoint:**
   ```bash
   curl -v http://localhost:8000/ws/
   ```
   Should return `400 Bad Request` (not a WebSocket upgrade request).

3. **Check browser console** for connection errors and reconnection attempts.

### Message Not Received

1. Verify the user is in the correct group (`user_{id}` or `broadcast`).
2. Check Redis connection in Django logs.
3. Ensure the message type matches between backend and frontend.

### Heartbeat Failures

If connections are dropping due to heartbeat failures:

1. Check network stability.
2. Verify nginx proxy timeout is sufficient (recommended: 86400s).
3. Check server load and Redis performance.

## Testing

Run WebSocket tests:

```bash
cd backend
uv run pytest core/tests/websocket/ -v
```

## Security Considerations

- JWT tokens expire and should be refreshed before WebSocket reconnection.
- Message size is limited to 64KB to prevent memory issues.
- Redis should not be exposed publicly; use internal networking.
- Always use WSS (WebSocket Secure) in production.

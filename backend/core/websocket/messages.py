from enum import Enum


class WebSocketMessageType(str, Enum):
    MESSAGE_CREATED = "MESSAGE_CREATED"
    MESSAGE_DELETED = "MESSAGE_DELETED"
    MESSAGE_VIEWED = "MESSAGE_VIEWED"
    USER_PRESENCE_CONNECTED = "USER_PRESENCE_CONNECTED"
    USER_PRESENCE_DISCONNECTED = "USER_PRESENCE_DISCONNECTED"
    BUCKETPOINT_CREATED = "BUCKETPOINT_CREATED"
    BUCKETPOINT_DELETED = "BUCKETPOINT_DELETED"
    BUCKETPOINT_UPDATED = "BUCKETPOINT_UPDATED"

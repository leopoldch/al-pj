import { WebSocketMessageType } from "./websockets.js";
import {
  MessageViewed,
  MessageCreated,
  MessageDeleted,
  Presence,
  BucketPointDeleted,
  BucketPointCreated,
  BucketPointUpdated,
} from "./websocket-interfaces.js";
export interface WebSocketMessageTable {
  [WebSocketMessageType.MessageViewed]: MessageViewed;
  [WebSocketMessageType.MessageCreated]: MessageCreated;
  [WebSocketMessageType.MessageDeleted]: MessageDeleted;
  [WebSocketMessageType.UserPresenceConnected]: Presence;
  [WebSocketMessageType.UserPresenceDisconnected]: Presence;
  // bucket points
  [WebSocketMessageType.BucketPointCreated]: BucketPointCreated;
  [WebSocketMessageType.BucketPointDeleted]: BucketPointDeleted;
  [WebSocketMessageType.BucketPointUpdated]: BucketPointUpdated;
}
export interface WebSocketMessage<T extends WebSocketMessageType> {
  type: T;
  data: WebSocketMessageTable[T];
}

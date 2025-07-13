import { WebSocketMessageType } from "./websockets.js";
import { MessageViewed, MessageCreated, MessageDeleted, Presence } from "./websocket-interfaces.js";
export interface WebSocketMessageTable {
  [WebSocketMessageType.MessageViewed]: MessageViewed;
  [WebSocketMessageType.MessageCreated]: MessageCreated;
  [WebSocketMessageType.MessageDeleted]: MessageDeleted;
  [WebSocketMessageType.UserPresenceConnected]: Presence;
  [WebSocketMessageType.UserPresenceDisconnected]: Presence;
}
export interface WebSocketMessage<T extends WebSocketMessageType> {
  type: T;
  data: WebSocketMessageTable[T];
}

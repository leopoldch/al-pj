import { WebSocketMessageType } from "./websockets.js";
import { MessageViewed, MessageCreated, MessageDeleted } from "./websocket-interfaces.js";
export interface WebSocketMessageTable {
  [WebSocketMessageType.MessageViewed]: MessageViewed;
  [WebSocketMessageType.MessageCreated]: MessageCreated;
  [WebSocketMessageType.MessageDeleted]: MessageDeleted;
}
export interface WebSocketMessage<T extends WebSocketMessageType> {
  type: T;
  data: WebSocketMessageTable[T];
}

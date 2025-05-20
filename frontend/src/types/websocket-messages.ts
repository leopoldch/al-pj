import { WebSocketMessageType } from "./websockets.js";
import { MessageViewed } from "./websocket-interfaces.js";
export interface WebSocketMessageTable {
  [WebSocketMessageType.MessageViewed]: MessageViewed;
}
export interface WebSocketMessage<T extends WebSocketMessageType> {
  type: T;
  data: WebSocketMessageTable[T];
}

import { WebSocketMessage, WebSocketMessageTable } from "../types/websocket-messages";
import { WebSocketMessageType } from "../types/websockets";

type WebSocketCallback<T extends WebSocketMessageType> = (data: WebSocketMessageTable[T]) => void;
type WebSocketCallbacks = {
  [key in WebSocketMessageType]: Set<WebSocketCallback<key>>;
};
const buildWebSocketCallbacks = (): WebSocketCallbacks => {
  const webSocketCallback = {} as WebSocketCallbacks;
  for (const messageType of Object.values(WebSocketMessageType)) {
    // TODO: type this properly to prevent mistakes
    // The end result of the function is still typed properly
    webSocketCallback[messageType] = new Set() as any;
  }
  return webSocketCallback;
};
export class WebSocketClient {
  private webSocket: WebSocket | null = null;
  private accessToken: string | null = null;
  private callbacks: WebSocketCallbacks = buildWebSocketCallbacks();
  private reconnectionTimeout: ReturnType<typeof setTimeout> | null = null;
  // Queue of messages waiting for connection
  // TODO: Add timeout (or something else) for messages that should be discarded when it takes too long
  private sendQueue: Parameters<WebSocketClient["send"]>[] = [];
  connect(apiUrl: string, accessToken: string) {
    if (this.accessToken === accessToken) {
      if (
        this.webSocket?.readyState === WebSocket.OPEN ||
        this.webSocket?.readyState === WebSocket.CONNECTING
      ) {
        return; // Connection is already OK
      }
    } else {
      // Clean up to make sure messages for previous token won't be sent or received accidentaly
      this.disconnect();
    }
    this.accessToken = accessToken;
    const url = new URL(apiUrl);
    url.protocol = "ws:";
    url.pathname = "/ws/";
    url.searchParams.set("accessToken", accessToken);
    this.webSocket = new WebSocket(url.toString());
    const webSocket = this.webSocket;
    webSocket.onopen = () => {
      console.debug("WebSocket connected");
      // Send queued messages
      const oldSendQueue = this.sendQueue;
      this.sendQueue = [];
      oldSendQueue.forEach(([type, data]) => this.send(type, data));
    };
    webSocket.onclose = (event) => {
      // Involuntary disconnection. See 'disconnect' method to disconnect voluntarily.
      console.debug(
        `WebSocket has been involuntarily disconnected (code: ${event.code}). Reconnecting...`
      );
      this.reconnectionTimeout = setTimeout(() => this.connect(apiUrl, accessToken), 2000);
    };
    webSocket.onmessage = <T extends WebSocketMessageType>(event: MessageEvent<string>) => {
      const messageString = event.data;
      const message: WebSocketMessage<T> = JSON.parse(messageString);
      console.debug("WebSocket received message", message);
      if (!message.type || !message.data) {
        console.warn(
          "WebSocket message is not a valid WebSocketMessage (missing type or data fields)"
        );
        return;
      }
      if (!Object.values(WebSocketMessageType).includes(message.type)) {
        console.warn(`Invalid WebSocket message type: ${message.type}`);
        return;
      }
      const callbacksForType = this.callbacks[message.type];
      for (const callback of callbacksForType) {
        callback(message.data);
      }
    };
    webSocket.onerror = (event: Event) => {
      console.error("WebSocket errored", event);
    };
  }
  disconnect() {
    // Cancel any previous reconnection attempt
    if (this.reconnectionTimeout) {
      clearTimeout(this.reconnectionTimeout);
      this.reconnectionTimeout = null;
    }
    this.sendQueue = [];
    this.accessToken = null;
    if (this.webSocket) {
      this.webSocket.onclose = (event) =>
        console.debug(`WebSocket has been voluntarily disconnected (code: ${event.code})`);
      this.webSocket.close();
      this.webSocket = null;
    }
  }
  bind<T extends WebSocketMessageType>(
    type: T,
    callback: (data: WebSocketMessageTable[T]) => void
  ) {
    const callbacksForType = this.callbacks[type];
    callbacksForType.add(callback);
  }
  unbind<T extends WebSocketMessageType>(
    type: T,
    callback: (data: WebSocketMessageTable[T]) => void
  ) {
    const callbacksForType = this.callbacks[type];
    callbacksForType.delete(callback);
  }
  send<T extends WebSocketMessageType>(type: T, data: WebSocketMessageTable[T]) {
    if (!this.webSocket || this.webSocket.readyState !== WebSocket.OPEN) {
      this.sendQueue.push([type, data]);
      return;
    }
    this.webSocket.send(JSON.stringify({ type, data }));
  }
}

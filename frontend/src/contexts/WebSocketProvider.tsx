import React, { ReactNode, useEffect, useMemo, useRef } from "react";
import { createOptionalContext } from "../hooks/createOptionnalContext";
import { WebSocketClient } from "../services/WebSocketClient";
import { useAuth } from "../hooks/useAuth";
export interface IWebSocketContext {
  bind: WebSocketClient["bind"];
  unbind: WebSocketClient["unbind"];
  send: WebSocketClient["send"];
}

type WithChildren = {
  children: ReactNode;
};

const optionalWebSocketContext = createOptionalContext<IWebSocketContext>("WebSocketContext");
export const useWebSocketContext = optionalWebSocketContext.useOptionalContext;
export default ({ children }: WithChildren) => {
  const webSocketClientRef = useRef<WebSocketClient>(new WebSocketClient());
  const { token: accessToken } = useAuth();
  const currentUrl = window.location.href;
  const wsUrl = process.env.NODE_ENV === "development" ? process.env.REACT_APP_WS_URL : currentUrl;
  if (!wsUrl) {
    throw new Error("WebSocket URL is not defined");
  }
  useEffect(() => {
    if (!accessToken) return;
    webSocketClientRef.current.connect(wsUrl, accessToken);
  }, [accessToken]);
  const value = useMemo(
    () => ({
      bind: webSocketClientRef.current.bind.bind(webSocketClientRef.current),
      unbind: webSocketClientRef.current.unbind.bind(webSocketClientRef.current),
      send: webSocketClientRef.current.send.bind(webSocketClientRef.current),
    }),
    []
  );
  return (
    <optionalWebSocketContext.Context.Provider value={value}>
      {children}
    </optionalWebSocketContext.Context.Provider>
  );
};

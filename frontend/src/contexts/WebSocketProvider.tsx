import React, { ReactNode, useEffect, useMemo, useRef, useState, useCallback } from "react"
import { createOptionalContext } from "../hooks/createOptionnalContext"
import { WebSocketClient, ConnectionStatus } from "../services/WebSocketClient"
import { useAuth } from "../hooks/useAuth"

export interface IWebSocketContext {
    bind: WebSocketClient["bind"]
    unbind: WebSocketClient["unbind"]
    send: WebSocketClient["send"]
    connectionStatus: ConnectionStatus
    isConnected: boolean
    forceReconnect: () => void
}

type WithChildren = {
    children: ReactNode
}

const optionalWebSocketContext = createOptionalContext<IWebSocketContext>("WebSocketContext")
export const useWebSocketContext = optionalWebSocketContext.useOptionalContext

const WebSocketProvider = ({ children }: WithChildren) => {
    const webSocketClientRef = useRef<WebSocketClient>(new WebSocketClient())
    const { token: accessToken } = useAuth()
    const currentUrl = window.location.origin
    const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>("disconnected")

    const wsUrl =
        process.env.NODE_ENV === "development" ? process.env.REACT_APP_WS_URL : `${currentUrl}/ws/`

    if (!wsUrl) {
        throw new Error("WebSocket URL is not defined")
    }

    let wsUrlFormatted = wsUrl
    if (wsUrlFormatted.startsWith("https://")) {
        wsUrlFormatted = wsUrlFormatted.replace("https://", "wss://")
    } else if (wsUrlFormatted.startsWith("http://")) {
        wsUrlFormatted = wsUrlFormatted.replace("http://", "ws://")
    }

    // Subscribe to connection status changes
    useEffect(() => {
        const unsubscribe = webSocketClientRef.current.onConnectionStatusChange((status) => {
            setConnectionStatus(status)
        })
        return unsubscribe
    }, [])

    // Connect when access token is available
    useEffect(() => {
        if (!accessToken) {
            webSocketClientRef.current.disconnect()
            return
        }
        webSocketClientRef.current.connect(wsUrlFormatted, accessToken)

        // Cleanup on unmount
        return () => {
            webSocketClientRef.current.disconnect()
        }
    }, [accessToken, wsUrlFormatted])

    const forceReconnect = useCallback(() => {
        webSocketClientRef.current.forceReconnect()
    }, [])

    const value = useMemo(
        () => ({
            bind: webSocketClientRef.current.bind.bind(webSocketClientRef.current),
            unbind: webSocketClientRef.current.unbind.bind(webSocketClientRef.current),
            send: webSocketClientRef.current.send.bind(webSocketClientRef.current),
            connectionStatus,
            isConnected: connectionStatus === "connected",
            forceReconnect,
        }),
        [connectionStatus, forceReconnect]
    )

    return (
        <optionalWebSocketContext.Context.Provider value={value}>
            {children}
        </optionalWebSocketContext.Context.Provider>
    )
}

export default WebSocketProvider

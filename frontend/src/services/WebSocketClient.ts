import { WebSocketMessage, WebSocketMessageTable } from "../types/websocket-messages"
import { WebSocketMessageType } from "../types/websockets"

type WebSocketCallback<T extends WebSocketMessageType> = (data: WebSocketMessageTable[T]) => void
type WebSocketCallbacks = {
    [key in WebSocketMessageType]: Set<WebSocketCallback<key>>
}

export type ConnectionStatus = "disconnected" | "connecting" | "connected" | "reconnecting"
type ConnectionStatusCallback = (status: ConnectionStatus) => void

// Configuration constants
const INITIAL_RECONNECT_DELAY = 1000 // 1 second
const MAX_RECONNECT_DELAY = 30000 // 30 seconds
const RECONNECT_MULTIPLIER = 1.5
const MAX_RECONNECT_ATTEMPTS = 20
const MESSAGE_QUEUE_MAX_SIZE = 100
const MESSAGE_QUEUE_MAX_AGE = 60000 // 1 minute

interface QueuedMessage {
    type: WebSocketMessageType
    data: unknown
    timestamp: number
}

const buildWebSocketCallbacks = (): WebSocketCallbacks => {
    const webSocketCallback = {} as WebSocketCallbacks
    for (const messageType of Object.values(WebSocketMessageType)) {
        webSocketCallback[messageType] = new Set() as never
    }
    return webSocketCallback
}

export class WebSocketClient {
    private webSocket: WebSocket | null = null
    private accessToken: string | null = null
    private apiUrl: string | null = null
    private callbacks: WebSocketCallbacks = buildWebSocketCallbacks()
    private reconnectionTimeout: ReturnType<typeof setTimeout> | null = null
    private reconnectAttempts = 0
    private currentReconnectDelay = INITIAL_RECONNECT_DELAY
    private sendQueue: QueuedMessage[] = []
    private connectionStatus: ConnectionStatus = "disconnected"
    private connectionStatusCallbacks: Set<ConnectionStatusCallback> = new Set()
    private isManualDisconnect = false

    /**
     * Get current connection status
     */
    getConnectionStatus(): ConnectionStatus {
        return this.connectionStatus
    }

    /**
     * Subscribe to connection status changes
     */
    onConnectionStatusChange(callback: ConnectionStatusCallback): () => void {
        this.connectionStatusCallbacks.add(callback)
        // Immediately notify of current status
        callback(this.connectionStatus)
        // Return unsubscribe function
        return () => {
            this.connectionStatusCallbacks.delete(callback)
        }
    }

    private setConnectionStatus(status: ConnectionStatus) {
        if (this.connectionStatus !== status) {
            this.connectionStatus = status
            this.connectionStatusCallbacks.forEach((cb) => cb(status))
        }
    }

    /**
     * Connect to WebSocket server
     */
    connect(apiUrl: string, accessToken: string) {
        if (this.accessToken === accessToken) {
            if (
                this.webSocket?.readyState === WebSocket.OPEN ||
                this.webSocket?.readyState === WebSocket.CONNECTING
            ) {
                return // Connection is already OK
            }
        } else {
            // Clean up to make sure messages for previous token won't be sent or received accidentally
            this.disconnect()
        }

        this.isManualDisconnect = false
        this.accessToken = accessToken
        this.apiUrl = apiUrl
        this.setConnectionStatus(this.reconnectAttempts > 0 ? "reconnecting" : "connecting")

        const url = new URL(apiUrl)

        // Use secure WebSocket for HTTPS, insecure for HTTP (dev)
        url.protocol = window.location.protocol === "https:" ? "wss:" : "ws:"
        url.searchParams.set("accessToken", accessToken)

        try {
            this.webSocket = new WebSocket(url.toString())
        } catch (error) {
            console.error("Failed to create WebSocket:", error)
            this.scheduleReconnect()
            return
        }

        const webSocket = this.webSocket

        webSocket.onopen = () => {
            console.debug("WebSocket connected")
            this.setConnectionStatus("connected")
            this.reconnectAttempts = 0
            this.currentReconnectDelay = INITIAL_RECONNECT_DELAY

            // Send queued messages (filter out expired ones)
            this.flushMessageQueue()
        }

        webSocket.onclose = (event) => {
            if (this.isManualDisconnect) {
                console.debug(`WebSocket disconnected voluntarily (code: ${event.code})`)
                this.setConnectionStatus("disconnected")
                return
            }

            // Involuntary disconnection
            console.debug(
                `WebSocket disconnected involuntarily (code: ${event.code}, reason: ${event.reason}). Scheduling reconnect...`
            )
            this.setConnectionStatus("reconnecting")
            this.scheduleReconnect()
        }

        webSocket.onmessage = <T extends WebSocketMessageType>(event: MessageEvent<string>) => {
            this.handleMessage(event)
        }

        webSocket.onerror = (event: Event) => {
            console.error("WebSocket error:", event)
        }
    }

    private handleMessage<T extends WebSocketMessageType>(event: MessageEvent<string>) {
        const messageString = event.data

        try {
            const message: WebSocketMessage<T> = JSON.parse(messageString)
            console.debug("WebSocket received message:", message.type)

            // Handle server PING - respond with PONG
            if (message.type === ("PING" as T)) {
                this.sendRaw({ type: "PONG", data: { timestamp: new Date().toISOString() } })
                return
            }

            // Handle ERROR messages
            if (message.type === ("ERROR" as T)) {
                console.warn("WebSocket error from server:", message.data)
                return
            }

            if (!message.type || message.data === undefined) {
                console.warn("WebSocket message is not valid (missing type or data fields)")
                return
            }

            if (!Object.values(WebSocketMessageType).includes(message.type)) {
                console.warn(`Unknown WebSocket message type: ${message.type}`)
                return
            }

            const callbacksForType = this.callbacks[message.type]
            for (const callback of callbacksForType) {
                try {
                    callback(message.data)
                } catch (error) {
                    console.error(`Error in WebSocket callback for ${message.type}:`, error)
                }
            }
        } catch (error) {
            console.error("Failed to parse WebSocket message:", error)
        }
    }

    private scheduleReconnect() {
        if (this.isManualDisconnect) {
            return
        }

        if (this.reconnectionTimeout) {
            clearTimeout(this.reconnectionTimeout)
        }

        if (this.reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
            console.error(
                `Max reconnection attempts (${MAX_RECONNECT_ATTEMPTS}) reached. Giving up.`
            )
            this.setConnectionStatus("disconnected")
            return
        }

        this.reconnectAttempts++

        // Exponential backoff with jitter
        const jitter = Math.random() * 0.3 * this.currentReconnectDelay
        const delay = Math.min(this.currentReconnectDelay + jitter, MAX_RECONNECT_DELAY)

        console.debug(
            `Scheduling reconnect attempt ${this.reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS} in ${Math.round(delay)}ms`
        )

        this.reconnectionTimeout = setTimeout(() => {
            if (this.apiUrl && this.accessToken) {
                this.connect(this.apiUrl, this.accessToken)
            }
        }, delay)

        // Increase delay for next attempt
        this.currentReconnectDelay = Math.min(
            this.currentReconnectDelay * RECONNECT_MULTIPLIER,
            MAX_RECONNECT_DELAY
        )
    }

    private flushMessageQueue() {
        const now = Date.now()
        // Filter out expired messages
        const validMessages = this.sendQueue.filter(
            (msg) => now - msg.timestamp < MESSAGE_QUEUE_MAX_AGE
        )

        this.sendQueue = []

        validMessages.forEach((msg) => {
            this.send(msg.type, msg.data as WebSocketMessageTable[typeof msg.type])
        })

        if (validMessages.length < this.sendQueue.length) {
            console.debug(
                `Dropped ${this.sendQueue.length - validMessages.length} expired queued messages`
            )
        }
    }

    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        this.isManualDisconnect = true

        // Cancel any pending reconnection
        if (this.reconnectionTimeout) {
            clearTimeout(this.reconnectionTimeout)
            this.reconnectionTimeout = null
        }

        this.sendQueue = []
        this.accessToken = null
        this.apiUrl = null
        this.reconnectAttempts = 0
        this.currentReconnectDelay = INITIAL_RECONNECT_DELAY

        if (this.webSocket) {
            this.webSocket.onclose = null // Prevent reconnection logic
            this.webSocket.close(1000, "Client disconnect")
            this.webSocket = null
        }

        this.setConnectionStatus("disconnected")
    }

    /**
     * Subscribe to a specific message type
     */
    bind<T extends WebSocketMessageType>(
        type: T,
        callback: (data: WebSocketMessageTable[T]) => void
    ) {
        const callbacksForType = this.callbacks[type]
        callbacksForType.add(callback)
    }

    /**
     * Unsubscribe from a specific message type
     */
    unbind<T extends WebSocketMessageType>(
        type: T,
        callback: (data: WebSocketMessageTable[T]) => void
    ) {
        const callbacksForType = this.callbacks[type]
        callbacksForType.delete(callback)
    }

    /**
     * Send a typed message to the server
     */
    send<T extends WebSocketMessageType>(type: T, data: WebSocketMessageTable[T]) {
        if (!this.webSocket || this.webSocket.readyState !== WebSocket.OPEN) {
            // Queue message for later if not connected
            if (this.sendQueue.length < MESSAGE_QUEUE_MAX_SIZE) {
                this.sendQueue.push({ type, data, timestamp: Date.now() })
            } else {
                console.warn("Message queue full, dropping message")
            }
            return
        }
        this.sendRaw({ type, data })
    }

    /**
     * Send raw data without queueing
     */
    private sendRaw(data: unknown) {
        if (this.webSocket?.readyState === WebSocket.OPEN) {
            this.webSocket.send(JSON.stringify(data))
        }
    }

    /**
     * Check if currently connected
     */
    isConnected(): boolean {
        return this.webSocket?.readyState === WebSocket.OPEN
    }

    /**
     * Force immediate reconnection attempt
     */
    forceReconnect() {
        if (this.apiUrl && this.accessToken) {
            this.reconnectAttempts = 0
            this.currentReconnectDelay = INITIAL_RECONNECT_DELAY
            this.disconnect()
            this.isManualDisconnect = false
            this.connect(this.apiUrl, this.accessToken)
        }
    }
}

import { Box } from "@mui/material"
import React, { useEffect, useState } from "react"
import FiberManualRecordIcon from "@mui/icons-material/FiberManualRecord"
import { useWebSocketContext } from "../contexts/WebSocketProvider"
import { useAuth } from "../hooks/useAuth"
import { WebSocketMessageType } from "../types/websockets"
import { Presence } from "../types/websocket-interfaces"
import { useGetPresence } from "../queries/presence"

function PresenceIndicator() {
    const [isOnline, setIsOnline] = useState(false)
    const [userName, setUserName] = useState<string | null>(null)

    const websocket = useWebSocketContext()
    const { user } = useAuth()
    const { data, isError, isLoading } = useGetPresence()

    useEffect(() => {
        if (!data || !user) return

        if (data.user_id !== user.id) {
            setIsOnline(data.is_online)
            setUserName(data.name)
        }
    }, [data, user])

    useEffect(() => {
        if (!userName || !user) return

        const handlePresence = (state: boolean) => (payload: Presence) => {
            if (payload.user_id !== user.id) {
                setIsOnline(state)
                setUserName(payload.name)
            }
        }

        const onConnect = handlePresence(true)
        const onDisconnect = handlePresence(false)

        websocket.bind(WebSocketMessageType.UserPresenceConnected, onConnect)
        websocket.bind(WebSocketMessageType.UserPresenceDisconnected, onDisconnect)

        return () => {
            websocket.unbind(WebSocketMessageType.UserPresenceConnected, onConnect)
            websocket.unbind(WebSocketMessageType.UserPresenceDisconnected, onDisconnect)
        }
    }, [websocket, userName, user?.id])

    if (isLoading) return <Box>Loading...</Box>
    if (isError || !userName) return <Box>Error loading presence data</Box>

    return (
        <Box
            sx={{
                display: "flex",
                alignItems: "center",
                gap: 1,
                backgroundColor: "#fffdf8",
                borderRadius: "20px",
                px: 2,
                py: 0.5,
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                fontFamily: "'Quicksand', sans-serif",
                fontWeight: 500,
                fontSize: "0.9rem",
                color: "#333",
                transition: "all 0.3s ease-in-out",
            }}
        >
            <Box
                sx={{
                    width: 10,
                    height: 10,
                    borderRadius: "50%",
                    backgroundColor: isOnline ? "#64d17a" : "#f47373",
                    transition: "background-color 0.3s ease",
                }}
            />
            <Box>{isOnline ? `${userName} is online` : `${userName} is offline`}</Box>
        </Box>
    )
}

export default PresenceIndicator

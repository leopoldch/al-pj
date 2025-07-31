import React, { useEffect, useState } from "react"
import { Box, IconButton, useMediaQuery, useTheme, Typography } from "@mui/material"
import DeleteIcon from "@mui/icons-material/Delete"
import { useDeleteMessage, useGetAllMessages } from "../queries/messages"
import { useAuth } from "../hooks/useAuth"
import { useWebSocketContext } from "../contexts/WebSocketProvider"
import { WebSocketMessageType } from "../types/websockets"
import { MessageCreated, MessageDeleted } from "../types/websocket-interfaces"
import Imessage from "../types/messages"

function DisplayAllMessages() {
    const { data: msgQuery } = useGetAllMessages()
    const deleteMessage = useDeleteMessage()
    const { user } = useAuth()
    const websocket = useWebSocketContext()

    const [messages, setMessages] = useState<Imessage[]>([])

    const theme = useTheme()
    const isMobile = useMediaQuery(theme.breakpoints.down("md"))

    useEffect(() => {
        if (msgQuery) setMessages(msgQuery)
    }, [msgQuery])

    useEffect(() => {
        const handleMessageCreated = (data: MessageCreated) => {
            setMessages((prev) => [data.message, ...prev])
        }

        const handleMessageDeleted = (data: MessageDeleted) => {
            setMessages((prev) => prev.filter((msg) => msg.id !== Number(data.message.id)))
        }

        websocket.bind(WebSocketMessageType.MessageCreated, handleMessageCreated)
        websocket.bind(WebSocketMessageType.MessageDeleted, handleMessageDeleted)
        websocket.bind(WebSocketMessageType.MessageViewed, () => {})

        return () => {
            websocket.unbind(WebSocketMessageType.MessageCreated, handleMessageCreated)
            websocket.unbind(WebSocketMessageType.MessageDeleted, handleMessageDeleted)
            websocket.unbind(WebSocketMessageType.MessageViewed, () => {})
        }
    }, [websocket])

    if (!messages) return <Box>Loading...</Box>

    const sortedMessages = [...messages].sort(
        (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )

    return (
        <Box
            sx={{
                width: isMobile ? "95%" : "80%",
                flexGrow: 1,
                minHeight: 0,
                maxHeight: isMobile ? "45vh" : "60vh",
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
                gap: theme.spacing(2),
                p: theme.spacing(1),
                mx: "auto",
            }}
        >
            {sortedMessages.length === 0 ? (
                <Box
                    sx={{
                        backgroundColor: "rgba(128, 128, 128, 0.1)",
                        p: theme.spacing(2),
                        borderRadius: 1,
                        textAlign: "center",
                    }}
                >
                    <Typography
                        variant="body1"
                        color="text.primary"
                        fontSize={isMobile ? "1rem" : "1.1rem"}
                    >
                        Aucun message trouvé.
                    </Typography>
                </Box>
            ) : (
                sortedMessages.map((message) => (
                    <Box
                        key={message.id}
                        sx={{
                            position: "relative",
                            p: isMobile ? 1.5 : 2,
                            backgroundColor: "#f9f9f9",
                            borderRadius: 2,
                            boxShadow: theme.shadows[1],
                            fontSize: isMobile ? "0.85rem" : "0.95rem",
                            wordBreak: "break-word",
                        }}
                    >
                        {user?.email === message.email && (
                            <IconButton
                                onClick={() => deleteMessage.mutate(message.id)}
                                sx={{
                                    position: "absolute",
                                    top: theme.spacing(1),
                                    right: theme.spacing(1),
                                    p: isMobile ? 0.5 : 1,
                                }}
                            >
                                <DeleteIcon fontSize={isMobile ? "small" : "medium"} />
                            </IconButton>
                        )}
                        <Typography fontWeight="bold" gutterBottom>
                            {message.name}
                        </Typography>
                        <Typography
                            sx={{
                                mb: theme.spacing(0.5),
                                whiteSpace: "pre-wrap",
                            }}
                        >
                            {message.message}
                        </Typography>
                        <Typography
                            variant="caption"
                            color="text.secondary"
                            fontSize={isMobile ? "0.7rem" : "0.75rem"}
                        >
                            {new Date(message.created_at).toLocaleString()}
                        </Typography>
                    </Box>
                ))
            )}
        </Box>
    )
}

export default DisplayAllMessages

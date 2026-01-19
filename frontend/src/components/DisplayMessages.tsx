import React, { useEffect } from "react"
import { Box, IconButton, useMediaQuery, useTheme, Typography } from "@mui/material"
import DeleteIcon from "@mui/icons-material/Delete"
import { useDeleteMessage, useGetPaginatedMessages } from "../queries/messages"
import { useAuth } from "../hooks/useAuth"
import { useWebSocketContext } from "../contexts/WebSocketProvider"
import { useQueryClient } from "@tanstack/react-query"
import { WebSocketMessageType } from "../types/websockets"
import { MessageCreated, MessageDeleted } from "../types/websocket-interfaces"
import Imessage, { PaginatedResponse } from "../types/messages"
import { Virtuoso } from "react-virtuoso"

function DisplayAllMessages() {
    const {
        data: msgQuery,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
    } = useGetPaginatedMessages()
    const deleteMessage = useDeleteMessage()
    const { user } = useAuth()
    const websocket = useWebSocketContext()
    const queryClient = useQueryClient()

    const theme = useTheme()
    const isMobile = useMediaQuery(theme.breakpoints.down("md"))

    useEffect(() => {
        const handleMessageCreated = (data: MessageCreated) => {
            queryClient.setQueryData(
                ["messages", "paginated"],
                (oldData: { pages: PaginatedResponse<Imessage>[] } | undefined) => {
                    if (!oldData) return oldData
                    const newPages = [...oldData.pages]
                    newPages[0] = {
                        ...newPages[0],
                        results: [data.message, ...newPages[0].results],
                        count: newPages[0].count + 1,
                    }
                    return { ...oldData, pages: newPages }
                }
            )
        }

        const handleMessageDeleted = (data: MessageDeleted) => {
            queryClient.setQueryData(
                ["messages", "paginated"],
                (oldData: { pages: PaginatedResponse<Imessage>[] } | undefined) => {
                    if (!oldData) return oldData
                    const newPages = oldData.pages.map((page) => ({
                        ...page,
                        results: page.results.filter(
                            (msg: Imessage) => msg.id !== Number(data.message.id)
                        ),
                    }))
                    return { ...oldData, pages: newPages }
                }
            )
        }

        websocket.bind(WebSocketMessageType.MessageCreated, handleMessageCreated)
        websocket.bind(WebSocketMessageType.MessageDeleted, handleMessageDeleted)
        websocket.bind(WebSocketMessageType.MessageViewed, () => {})

        return () => {
            websocket.unbind(WebSocketMessageType.MessageCreated, handleMessageCreated)
            websocket.unbind(WebSocketMessageType.MessageDeleted, handleMessageDeleted)
            websocket.unbind(WebSocketMessageType.MessageViewed, () => {})
        }
    }, [websocket, queryClient])

    const messages =
        msgQuery?.pages.flatMap((page: PaginatedResponse<Imessage>) => page.results) || []

    return (
        <Box
            sx={{
                width: isMobile ? "95%" : "80%",
                flexGrow: 1,
                minHeight: 0,
                height: isMobile ? "45vh" : "60vh",
                display: "flex",
                flexDirection: "column",
                gap: theme.spacing(2),
                p: theme.spacing(1),
                mx: "auto",
            }}
        >
            {messages.length === 0 ? (
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
                <Virtuoso
                    style={{ height: "100%", width: "100%" }}
                    data={messages}
                    endReached={() => {
                        if (hasNextPage && !isFetchingNextPage) {
                            fetchNextPage()
                        }
                    }}
                    overscan={1000}
                    itemContent={(index, message) => (
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
                                mb: 2,
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
                    )}
                />
            )}
        </Box>
    )
}

export default DisplayAllMessages

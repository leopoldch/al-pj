import { useDeleteMessage, useGetAllMessages } from "../queries/messages";
import { IconButton, Box } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import React, { useEffect } from "react";
import { useAuth } from "../hooks/useAuth";
import { useWebSocketContext } from "../contexts/WebSocketProvider";
import { WebSocketMessageType } from "../types/websockets";
import { MessageCreated, MessageDeleted, MessageViewed } from "../types/websocket-interfaces";

function DisplayAllMessages() {
  const { data: msgQuery } = useGetAllMessages();
  const [messages, setMessages] = React.useState<Imessage[]>([]);

  useEffect(() => {
    if (msgQuery) {
      setMessages(msgQuery);
    }
  }, [msgQuery]);

  const deleteMessage = useDeleteMessage();
  const { user } = useAuth();
  const handleDelete = (id: number) => {
    deleteMessage.mutate(id);
  };

  const websocket = useWebSocketContext();

  useEffect(() => {
    const handleMessageCreated = (data: MessageCreated) => {
      console.log("Message created:", data);
      // add at the beginning of the messages array
      setMessages((prev) => (prev ? [data.message, ...prev] : [data.message]));
    };

    const handleMessageViewed = (data: MessageViewed) => {
      console.log("Message updated:", data);
      // for now not used
    };

    const handleMessageDeleted = (data: MessageDeleted) => {
      console.log("Message deleted:", data);
      setMessages(
        (prev) => prev?.filter((message) => message.id !== Number(data.message.id)) || []
      );
    };

    websocket.bind(WebSocketMessageType.MessageCreated, handleMessageCreated);
    websocket.bind(WebSocketMessageType.MessageViewed, handleMessageViewed);
    websocket.bind(WebSocketMessageType.MessageDeleted, handleMessageDeleted);

    return () => {
      websocket.unbind(WebSocketMessageType.MessageCreated, handleMessageCreated);
      websocket.unbind(WebSocketMessageType.MessageViewed, handleMessageViewed);
      websocket.unbind(WebSocketMessageType.MessageDeleted, handleMessageDeleted);
    };
  }, [websocket]);

  if (!messages) {
    return <div>Loading...</div>;
  }

  const sortedMessages = [...messages].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  return (
    <Box
      sx={{
        maxHeight: "500px",
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
        gap: "1rem",
        p: "1rem",
        border: "1px solid #ccc",
        borderRadius: "8px",
        width: "80%",
      }}
    >
      {sortedMessages.length === 0 ? (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100%",
            fontSize: "1.2rem",
            color: "black",
            backgroundColor: "rgba(128, 128, 128, 0.1)",
          }}
        >
          Aucun message trouvé.
        </Box>
      ) : (
        sortedMessages.map((message) => (
          <Box
            key={message.id}
            sx={{
              position: "relative",
              p: "1rem",
              backgroundColor: "#f9f9f9",
              borderRadius: "8px",
              boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
            }}
          >
            {user?.username === message.name && (
              <IconButton
                onClick={() => handleDelete(message.id)}
                sx={{
                  position: "absolute",
                  top: "8px",
                  right: "8px",
                }}
              >
                <DeleteIcon />
              </IconButton>
            )}
            <Box sx={{ fontWeight: "bold" }}>{message.name}</Box>
            <Box sx={{ my: "0.5rem" }}>{message.message}</Box>
            <Box sx={{ fontSize: "0.8rem", color: "#666" }}>
              {new Date(message.created_at).toLocaleString()}
            </Box>
          </Box>
        ))
      )}
    </Box>
  );
}

export default DisplayAllMessages;

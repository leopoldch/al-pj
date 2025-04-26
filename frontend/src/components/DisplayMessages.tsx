import { useDeleteMessage, useGetAllMessages } from "../queries/messages";
import { IconButton, Box } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import React from "react";
import { useAuth } from "../hooks/useAuth";

function DisplayAllMessages() {
  const { data: messages } = useGetAllMessages();
  const deleteMessage = useDeleteMessage();
  const { user } = useAuth();
  const handleDelete = (id: number) => {
    deleteMessage.mutate(id);
  };

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

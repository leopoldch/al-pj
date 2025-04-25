import React from "react"
import { Box, TextField, IconButton, InputAdornment } from "@mui/material"
import SendIcon from "@mui/icons-material/Send"
import { usePostMessage } from "../queries/messages"

function MainInput() {
  const [message, setMessage] = React.useState("")
  const postMessage = usePostMessage()

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value)
  }

  const handleSubmit = () => {
    if (message.trim() !== "") {
      postMessage.mutate(message)
      console.log("Message submitted:", message)
      setMessage("")
    }
  }

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === "Enter") {
      event.preventDefault()
      handleSubmit()
    }
  }

  return (
    <Box
      sx={{
        marginTop: "-200px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "transparent",
        width: "400px",
        height: "300px",
      }}
    >
      <TextField
        type="text"
        placeholder="Écris quelque chose de mignon ici..."
        variant="outlined"
        fullWidth
        value={message}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        sx={{
          backgroundColor: "white",
          borderRadius: 2,
          boxShadow: 3,
          "& .MuiOutlinedInput-root": {
            borderRadius: 2,
            "& fieldset": {
              border: "none", // Retire la bordure normale
            },
            "&:hover fieldset": {
              border: "none", // Retire la bordure au hover
            },
            "&.Mui-focused fieldset": {
              border: "none", // Retire la bordure au focus
            },
            paddingRight: "0", // Ajuste pour que l'icône ne décale pas trop
          },
          input: {
            padding: "12px",
          },
        }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                onClick={handleSubmit}
                color="primary"
                edge="end"
                sx={{
                  backgroundColor: "primary.light",
                  color: "white",
                  "&:hover": {
                    backgroundColor: "primary.main",
                  },
                  borderRadius: 2,
                  marginRight: "4px",
                }}
              >
                <SendIcon />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    </Box>
  )
}

export default MainInput

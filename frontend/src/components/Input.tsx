import React from "react"
import { Box, TextField, IconButton, InputAdornment, useTheme, useMediaQuery } from "@mui/material"
import SendIcon from "@mui/icons-material/Send"
import { usePostMessage } from "../queries/messages"

function MainInput() {
    const [message, setMessage] = React.useState("")
    const postMessage = usePostMessage()

    const theme = useTheme()
    const isMobile = useMediaQuery(theme.breakpoints.down("md"))

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setMessage(event.target.value)
    }

    const handleSubmit = () => {
        const trimmed = message.trim()
        if (trimmed !== "") {
            postMessage.mutate(trimmed)
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
                width: isMobile ? "90%" : "400px",
                px: isMobile ? 1 : 0,
                py: 1,
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
                        "& fieldset": { border: "none" },
                        "&:hover fieldset": { border: "none" },
                        "&.Mui-focused fieldset": { border: "none" },
                    },
                    input: {
                        padding: theme.spacing(1.25),
                        fontSize: isMobile ? "0.9rem" : "1rem",
                    },
                }}
                InputProps={{
                    endAdornment: (
                        <InputAdornment position="end">
                            <IconButton
                                onClick={handleSubmit}
                                sx={{
                                    backgroundColor: "primary.light",
                                    color: "#fff",
                                    borderRadius: 2,
                                    width: theme.spacing(isMobile ? 4.5 : 5),
                                    height: theme.spacing(isMobile ? 4.5 : 5),
                                    "&:hover": {
                                        backgroundColor: "primary.main",
                                    },
                                    ml: 0.5,
                                    marginRight: -1.5,
                                }}
                            >
                                <SendIcon fontSize={isMobile ? "small" : "medium"} />
                            </IconButton>
                        </InputAdornment>
                    ),
                }}
            />
        </Box>
    )
}

export default MainInput

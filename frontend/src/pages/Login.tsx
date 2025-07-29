import { Box, Card, TextField, Button, Typography } from "@mui/material"
import React, { useEffect } from "react"
import { useLogin } from "../queries/auth"
import { useNavigate } from "react-router-dom"
import Footer from "../components/Footer"

function Login() {
    const [username, setUsername] = React.useState("")
    const [password, setPassword] = React.useState("")
    const [error, setError] = React.useState("")
    const loginMutation = useLogin()
    const navigate = useNavigate()

    useEffect(() => {
        const handleEnterKey: (e: KeyboardEvent) => void = (e: KeyboardEvent) => {
            if (e.key === "Enter") {
                handleSubmit(new Event("submit") as unknown as React.FormEvent)
            }
        }
        window.addEventListener("keydown", handleEnterKey)
        return () => {
            window.removeEventListener("keydown", handleEnterKey)
        }
    }, [username, password])

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (!username || !password) {
            setError("Veuillez remplir tous les champs.")
            return
        }
        setError("")

        loginMutation.mutate(
            { username, password },
            {
                onSuccess: () => {
                    navigate("/")
                },
                onError: (error) => {
                    setError("Une erreur s'est produite lors de la connexion.")
                    console.error(error)
                },
            }
        )
    }

    return (
        <Box
            sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                minHeight: "100vh",
                p: 2,
                flexDirection: "column",
                paddingTop: "200px",
            }}
        >
            <Card
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    gap: 2,
                    width: 400,
                    p: 4,
                    borderRadius: 3,
                    boxShadow: 6,
                    backdropFilter: "blur(5px)",
                    backgroundColor: "rgba(255, 255, 255, 0.8)",
                }}
            >
                <Typography variant="h4" align="center" fontWeight="bold">
                    Connexion
                </Typography>
                {error && (
                    <Typography color="error" align="center">
                        {error}
                    </Typography>
                )}
                <TextField
                    label="Nom d'utilisateur"
                    variant="outlined"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    fullWidth
                />
                <TextField
                    label="Mot de passe"
                    type="password"
                    variant="outlined"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    fullWidth
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                    fullWidth
                    disabled={loginMutation.isPending}
                >
                    {loginMutation.isPending ? "Connexion..." : "Se connecter"}
                </Button>
            </Card>
            <Footer />
        </Box>
    )
}

export default Login

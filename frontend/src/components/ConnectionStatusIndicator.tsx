import React from "react"
import { Box, Tooltip, CircularProgress, Fade } from "@mui/material"
import WifiIcon from "@mui/icons-material/Wifi"
import WifiOffIcon from "@mui/icons-material/WifiOff"
import SyncIcon from "@mui/icons-material/Sync"
import { useWebSocketContext } from "../contexts/WebSocketProvider"
import { ConnectionStatus } from "../services/WebSocketClient"

interface StatusConfig {
    icon: React.ReactNode
    color: string
    tooltip: string
}

const statusConfigs: Record<ConnectionStatus, StatusConfig> = {
    connected: {
        icon: <WifiIcon fontSize="small" />,
        color: "#4caf50",
        tooltip: "Connexion temps reel active",
    },
    connecting: {
        icon: <CircularProgress size={16} sx={{ color: "#ff9800" }} />,
        color: "#ff9800",
        tooltip: "Connexion en cours...",
    },
    reconnecting: {
        icon: <SyncIcon fontSize="small" sx={{ animation: "spin 1s linear infinite" }} />,
        color: "#ff9800",
        tooltip: "Reconnexion en cours...",
    },
    disconnected: {
        icon: <WifiOffIcon fontSize="small" />,
        color: "#f44336",
        tooltip: "Deconnecte - Les mises a jour temps reel sont desactivees",
    },
}

interface ConnectionStatusIndicatorProps {
    showLabel?: boolean
    size?: "small" | "medium"
}

const ConnectionStatusIndicator = ({
    showLabel = false,
    size = "small",
}: ConnectionStatusIndicatorProps) => {
    const { connectionStatus, forceReconnect } = useWebSocketContext()
    const config = statusConfigs[connectionStatus]

    const handleClick = () => {
        if (connectionStatus === "disconnected") {
            forceReconnect()
        }
    }

    return (
        <Tooltip title={config.tooltip} arrow>
            <Box
                onClick={handleClick}
                sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 0.5,
                    px: size === "small" ? 1 : 1.5,
                    py: size === "small" ? 0.5 : 0.75,
                    borderRadius: 2,
                    backgroundColor: `${config.color}20`,
                    color: config.color,
                    cursor: connectionStatus === "disconnected" ? "pointer" : "default",
                    transition: "all 0.2s",
                    "&:hover":
                        connectionStatus === "disconnected"
                            ? {
                                  backgroundColor: `${config.color}30`,
                              }
                            : {},
                    "@keyframes spin": {
                        "0%": { transform: "rotate(0deg)" },
                        "100%": { transform: "rotate(360deg)" },
                    },
                }}
            >
                {config.icon}
                {showLabel && (
                    <Fade in={true}>
                        <Box
                            component="span"
                            sx={{
                                fontSize: size === "small" ? 12 : 14,
                                fontWeight: 500,
                            }}
                        >
                            {connectionStatus === "connected" && "Connecte"}
                            {connectionStatus === "connecting" && "Connexion..."}
                            {connectionStatus === "reconnecting" && "Reconnexion..."}
                            {connectionStatus === "disconnected" && "Deconnecte"}
                        </Box>
                    </Fade>
                )}
            </Box>
        </Tooltip>
    )
}

export default ConnectionStatusIndicator

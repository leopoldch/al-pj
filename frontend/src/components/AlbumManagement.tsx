import { Box } from "@mui/material"
import React from "react"
import AddAlbumButton from "./AddAlbumButton"

export default function AlbumManagement() {
    return (
        <Box
            sx={{
                width: "100%",
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
                gap: 2,
            }}
        >
            <AddAlbumButton />
        </Box>
    )
}

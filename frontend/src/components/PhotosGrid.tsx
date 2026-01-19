import React from "react"
import { usePhotosWithWebSocket } from "../hooks/usePhotosWithWebSocket"
import PhotoCard from "./PhotoCard"
import { Grid, Typography, CircularProgress, Box, Fade } from "@mui/material"

const PhotosGrid = ({ id_album }: { id_album: string }) => {
    const { photos, isLoading, isError } = usePhotosWithWebSocket(id_album ?? "")

    if (isLoading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
                <CircularProgress />
            </Box>
        )
    }

    if (isError) {
        return (
            <Typography color="error" align="center">
                Erreur lors du chargement des photos.
            </Typography>
        )
    }

    if (photos.length === 0) {
        return (
            <Typography variant="body1" align="center">
                Aucun media pour cet album.
            </Typography>
        )
    }

    return (
        <Grid container spacing={2} justifyContent="center">
            {photos.map((photo, index) => (
                <Fade
                    key={photo.id}
                    in={true}
                    timeout={300 + index * 50}
                    style={{ transitionDelay: `${index * 30}ms` }}
                >
                    <Grid item>
                        <PhotoCard photo={photo} albumId={id_album} />
                    </Grid>
                </Fade>
            ))}
        </Grid>
    )
}

export default PhotosGrid

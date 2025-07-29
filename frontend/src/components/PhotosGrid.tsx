import React from "react"
import { useGetPhotos } from "../queries/photos"
import PhotoCard from "./PhotoCard"
import { Grid, Typography, CircularProgress, Box } from "@mui/material"

const PhotosGrid = ({ id_album }: { id_album: string }) => {
    const { data, isLoading, isError } = useGetPhotos(id_album ?? "")

    if (isLoading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
                <CircularProgress />
            </Box>
        )
    }

    if (isError || !data) {
        return (
            <Typography color="error" align="center">
                Erreur lors du chargement des photos.
            </Typography>
        )
    }

    if (data.photos.length === 0) {
        return (
            <Typography variant="body1" align="center">
                Aucun média pour cet album.
            </Typography>
        )
    }

    return (
        <Grid container spacing={2} justifyContent="center">
            {data.photos.map((photo) => (
                <Grid item key={photo.id}>
                    <PhotoCard photo={photo} />
                </Grid>
            ))}
        </Grid>
    )
}

export default PhotosGrid

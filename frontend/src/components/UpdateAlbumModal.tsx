import React, { useState } from "react"
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    IconButton,
    Stack,
} from "@mui/material"
import EditIcon from "@mui/icons-material/Edit"
import { useUpdateAlbumMutation } from "../queries/albums"
import { Album } from "../types/album"

function AlbumEditModal({ album }: { album: Album }) {
    const [open, setOpen] = useState(false)
    const [title, setTitle] = useState(album.title)
    const [description, setDescription] = useState(album.description)
    const [image, setImage] = useState<File | null>(null)

    const updateAlbumMutation = useUpdateAlbumMutation()

    const handleSubmit = () => {
        updateAlbumMutation.mutate({
            id: album.id,
            title,
            description,
            image: image || undefined,
        })
        setOpen(false)
    }

    return (
        <>
            <IconButton onClick={() => setOpen(true)} size="small">
                <EditIcon fontSize="small" />
            </IconButton>

            <Dialog open={open} onClose={() => setOpen(false)}>
                <DialogTitle>Modifier l&apos;album</DialogTitle>
                <DialogContent>
                    <Stack spacing={2} mt={1}>
                        <TextField
                            label="Titre"
                            value={title}
                            fullWidth
                            onChange={(e) => setTitle(e.target.value)}
                        />
                        <TextField
                            label="Description"
                            value={description}
                            fullWidth
                            multiline
                            rows={3}
                            onChange={(e) => setDescription(e.target.value)}
                        />
                        <Button variant="outlined" component="label">
                            {image ? image.name : "Changer l'image"}
                            <input
                                type="file"
                                hidden
                                accept="image/*"
                                onChange={(e) => {
                                    if (e.target.files?.[0]) {
                                        setImage(e.target.files[0])
                                    }
                                }}
                            />
                        </Button>
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpen(false)}>Annuler</Button>
                    <Button
                        onClick={handleSubmit}
                        variant="contained"
                        disabled={updateAlbumMutation.isPending}
                    >
                        Enregistrer
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    )
}

export default AlbumEditModal

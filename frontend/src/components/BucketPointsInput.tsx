import React, { useState } from "react"
import {
    Box,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Stack,
} from "@mui/material"
import { useCreateBucketPointMutation } from "../queries/bucketpoints"

export default function BucketPointsInput() {
    const [openModal, setOpenModal] = useState(false)
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const createBucketPoint = useCreateBucketPointMutation()

    const handleCreate = () => {
        if (title.trim() && description.trim()) {
            createBucketPoint.mutate({
                title,
                description,
                completed: false,
                id: 0, // backend will assign an ID
                created_at: new Date().toISOString(), // backend will assign a created_at timestamp
            })
            setOpenModal(false)
            setTitle("")
            setDescription("")
        }
    }

    return (
        <Box>
            <Button variant="contained" onClick={() => setOpenModal(true)}>
                Ajouter un Bucket Point
            </Button>

            <Dialog open={openModal} onClose={() => setOpenModal(false)}>
                <DialogTitle>Créer un nouveau Bucket Point</DialogTitle>
                <DialogContent>
                    <Stack spacing={2} mt={1}>
                        <TextField
                            label="Titre"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            fullWidth
                        />
                        <TextField
                            label="Description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            fullWidth
                        />
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenModal(false)}>Annuler</Button>
                    <Button variant="contained" onClick={handleCreate}>
                        Créer
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    )
}

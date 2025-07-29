import React, { useState } from "react";
import { Box, Button, Modal, TextField, Typography, Stack } from "@mui/material";
import { useAddAlbumMutation } from "../queries/albums";
import { AddAlbumInput } from "../types/album";

export default function AddAlbumButton() {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [image, setImage] = useState<File | null>(null);

  const addAlbumMutation = useAddAlbumMutation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const data: AddAlbumInput = {
        name: name,
        image: image ?? undefined,
        description: description,
      };

      await addAlbumMutation.mutateAsync(data);

      setModalIsOpen(false);
      setName("");
      setDescription("");
      setImage(null);
    } catch (err) {
      console.error("Erreur lors de l'ajout de l'album :", err);
    }
  };

  return (
    <>
      <Button variant="contained" onClick={() => setModalIsOpen(true)}>
        Ajouter un album
      </Button>

      <Modal open={modalIsOpen} onClose={() => setModalIsOpen(false)}>
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{
            position: "absolute" as const,
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            bgcolor: "background.paper",
            boxShadow: 24,
            p: 4,
            borderRadius: 2,
            width: "90%",
            maxWidth: 400,
          }}
        >
          <Typography variant="h6" gutterBottom>
            Ajouter un album
          </Typography>

          <Stack spacing={2}>
            <TextField
              label="Nom de l'album"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              fullWidth
            />

            <TextField
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              multiline
              rows={2}
              fullWidth
            />

            <Button variant="outlined" component="label">
              {image ? "Image sélectionnée" : "Choisir une image"}
              <input
                type="file"
                accept="image/*"
                hidden
                onChange={(e) => {
                  if (e.target.files && e.target.files.length > 0) {
                    setImage(e.target.files[0]);
                  }
                }}
              />
            </Button>

            <Box display="flex" justifyContent="flex-end" gap={1}>
              <Button onClick={() => setModalIsOpen(false)}>Annuler</Button>
              <Button type="submit" variant="contained">
                Ajouter
              </Button>
            </Box>
          </Stack>
        </Box>
      </Modal>
    </>
  );
}

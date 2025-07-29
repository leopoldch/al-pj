import React, { useState } from "react";
import { Box, Button, Modal, TextField, Typography, Stack } from "@mui/material";
import { useAddPhotoMutation } from "../queries/photos";
import { AddPhotoInput } from "../types/photo";

interface AddPhotoButtonProps {
  albumId: string;
}

export default function AddPhotoButton({ albumId }: AddPhotoButtonProps) {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [caption, setCaption] = useState<string>("");
  const [location, setLocation] = useState<string>("");
  const [image, setImage] = useState<File | null>(null);

  const addPhotoMutation = useAddPhotoMutation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const data: AddPhotoInput = {
        albumId: albumId,
        image: image!,
        caption: caption || undefined,
        location: location || undefined,
      };

      await addPhotoMutation.mutateAsync(data);

      setModalIsOpen(false);
      setCaption("");
      setLocation("");
      setImage(null);
    } catch (err) {
      console.error("Erreur lors de l'ajout de la photo :", err);
    }
  };

  return (
    <>
      <Button variant="contained" onClick={() => setModalIsOpen(true)}>
        Ajouter une photo
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
            Ajouter une photo
          </Typography>

          <Stack spacing={2}>
            <TextField
              label="Légende"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              fullWidth
            />

            <TextField
              label="Lieu"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              fullWidth
            />

            <Button variant="outlined" component="label">
              {image ? "Image sélectionnée" : "Choisir une image"}
              <input
                type="file"
                accept="image/*"
                hidden
                required
                onChange={(e) => {
                  if (e.target.files && e.target.files.length > 0) {
                    setImage(e.target.files[0]);
                  }
                }}
              />
            </Button>

            <Box display="flex" justifyContent="flex-end" gap={1}>
              <Button onClick={() => setModalIsOpen(false)}>Annuler</Button>
              <Button type="submit" variant="contained" disabled={!image}>
                Ajouter
              </Button>
            </Box>
          </Stack>
        </Box>
      </Modal>
    </>
  );
}

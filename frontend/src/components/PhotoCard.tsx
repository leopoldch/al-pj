import React, { useState } from "react";
import { Card, CardMedia, Typography, Box, Stack, Modal, Backdrop, useTheme } from "@mui/material";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import InsertPhotoIcon from "@mui/icons-material/InsertPhoto";

export interface Photo {
  id: number;
  album: string;
  image_url: string;
  caption: string;
  created_at: string;
  updated_at: string;
  location: string;
}

interface PhotoCardProps {
  photo: Photo;
}

const PhotoCard = ({ photo }: PhotoCardProps) => {
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const theme = useTheme();
  const isMobile = theme.breakpoints.down("sm");

  return (
    <>
      <Card
        sx={{
          width: 240,
          height: 240,
          position: "relative",
          borderRadius: 2,
          boxShadow: 3,
          overflow: "hidden",
          backgroundColor: "white",
          cursor: "pointer",
        }}
        onClick={handleOpen}
      >
        {photo.image_url ? (
          <CardMedia
            component="img"
            image={photo.image_url}
            alt={photo.caption || "Photo"}
            sx={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <Box
            sx={{
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "#f0f0f0",
            }}
          >
            <InsertPhotoIcon sx={{ fontSize: 48, color: "#bdbdbd" }} />
          </Box>
        )}

        <Box
          sx={{
            position: "absolute",
            bottom: 0,
            left: 0,
            width: "100%",
            px: 1,
            pb: 0.5,
            background: "linear-gradient(to top, rgba(0,0,0,0.5), rgba(0,0,0,0))",
          }}
        >
          <Stack spacing={0.3}>
            {photo.caption && (
              <Box
                sx={{
                  backgroundColor: "rgba(48, 48, 48, 0.5)",
                  borderRadius: 1,
                  px: 0.5,
                  py: 0.1,
                  width: "fit-content",
                }}
              >
                <Typography variant="caption" color="white" noWrap>
                  {photo.caption}
                </Typography>
              </Box>
            )}
            {photo.location && (
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  gap: 0.5,
                  backgroundColor: "rgba(48, 48, 48, 0.5)",
                  borderRadius: 1,
                  px: 0.5,
                  py: 0.1,
                  width: "fit-content",
                }}
              >
                <LocationOnIcon fontSize="small" sx={{ color: "white" }} />
                <Typography variant="caption" color="white" noWrap>
                  {photo.location}
                </Typography>
              </Box>
            )}
            <Box
              sx={{
                backgroundColor: "rgba(48, 48, 48, 0.5)",
                borderRadius: 1,
                px: 0.5,
                py: 0.1,
                width: "fit-content",
              }}
            >
              <Typography variant="caption" color="white" noWrap>
                {new Date(photo.created_at).toLocaleDateString("fr-FR")}
              </Typography>
            </Box>
          </Stack>
        </Box>
      </Card>

      <Modal
        open={open}
        onClose={handleClose}
        closeAfterTransition
        slots={{ backdrop: Backdrop }}
        slotProps={{
          backdrop: {
            timeout: 300,
            sx: { backgroundColor: "rgba(0,0,0,0.7)" },
          },
        }}
      >
        <Box
          sx={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            p: 2,
            boxSizing: "border-box",
          }}
        >
          {/* Bouton de fermeture global (haut-droite écran) */}
          <Box
            onClick={handleClose}
            sx={{
              position: "fixed",
              top: 16,
              right: 16,
              zIndex: 1301,
              backgroundColor: "rgba(0,0,0,0.6)",
              borderRadius: "50%",
              width: 36,
              height: 36,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
            }}
          >
            <Typography color="white" fontWeight="bold" fontSize={20}>
              ×
            </Typography>
          </Box>

          {/* Conteneur image + infos */}
          <Box
            sx={{
              maxWidth: { xs: "95vw", sm: "90vw", md: "70vw" },
              maxHeight: { xs: "90vh", sm: "85vh", md: "80vh" },
              display: "flex",
              flexDirection: "column",
              borderRadius: 2,
              overflow: "hidden",
              boxShadow: 5,
              backgroundColor: "#1e1e1e",
            }}
          >
            {/* Image */}
            <Box
              component="img"
              src={photo.image_url}
              alt={photo.caption || "Photo"}
              sx={{
                width: "100%",
                height: "auto",
                objectFit: "contain",
                maxHeight: "calc(80vh - 48px)", // 48px = hauteur de la barre infos
                backgroundColor: "black",
              }}
            />

            {/* Footer d'informations */}
            <Box
              sx={{
                width: "100%",
                backgroundColor: "rgba(0, 0, 0, 0.8)",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                px: 2,
                py: 1,
                color: "white",
                fontSize: 14,
              }}
            >
              {/* Légende et lieu */}
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  gap: 2,
                  flexWrap: "wrap",
                }}
              >
                {photo.caption && (
                  <Typography variant="body2" color="white" sx={{ whiteSpace: "nowrap" }}>
                    {photo.caption}
                  </Typography>
                )}
                {photo.location && (
                  <Box display="flex" alignItems="center" gap={0.5}>
                    <LocationOnIcon fontSize="small" sx={{ color: "white" }} />
                    <Typography variant="body2" color="white" sx={{ whiteSpace: "nowrap" }}>
                      {photo.location}
                    </Typography>
                  </Box>
                )}
              </Box>

              {/* Date */}
              <Typography variant="caption" color="white" sx={{ whiteSpace: "nowrap" }}>
                {new Date(photo.created_at).toLocaleDateString("fr-FR")}
              </Typography>
            </Box>
          </Box>
        </Box>
      </Modal>
    </>
  );
};

export default PhotoCard;

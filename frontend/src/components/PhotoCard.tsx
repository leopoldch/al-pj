import React, { useState } from "react";
import { Card, CardMedia, Typography, Box, Stack, Modal, Backdrop } from "@mui/material";
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
            position: "absolute" as const,
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            maxWidth: "90vw",
            maxHeight: "90vh",
            outline: "none",
          }}
        >
          <Box
            component="img"
            src={photo.image_url}
            alt={photo.caption || "Photo"}
            sx={{
              width: "100%",
              height: "auto",
              borderRadius: 2,
              maxHeight: "80vh",
              display: "block",
            }}
          />

          <Stack spacing={1} mt={2} px={1} color="white" alignItems="flex-start">
            {photo.caption && <Typography variant="body2">{photo.caption}</Typography>}
            {photo.location && (
              <Box display="flex" alignItems="center" gap={0.5}>
                <LocationOnIcon fontSize="small" />
                <Typography variant="body2">{photo.location}</Typography>
              </Box>
            )}
            <Typography variant="caption">
              {new Date(photo.created_at).toLocaleDateString("fr-FR")}
            </Typography>
          </Stack>
        </Box>
      </Modal>
    </>
  );
};

export default PhotoCard;

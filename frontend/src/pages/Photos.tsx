import React from "react";
import { Box, Typography } from "@mui/material";

import PageWrapper from "../components/PageWrapper";
import { useParams } from "react-router-dom";
import PhotosGrid from "../components/PhotosGrid";
import AddPhotoButton from "../components/AddPhotoButton";

function Albums() {
  const { id_album } = useParams<{ id_album: string }>();

  if (!id_album) {
    return (
      <PageWrapper>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
          <Typography variant="h6">Aucun album sélectionné.</Typography>
        </Box>
      </PageWrapper>
    );
  }

  return (
    <PageWrapper>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          gap: 2,
          width: "100%",
          px: 2,
          py: 4,
        }}
      >
        <Box sx={{ width: "100%", display: "flex", justifyContent: "center" }}>
          <Box sx={{ display: "flex", justifyContent: "flex-end", width: "80%" }}>
            <AddPhotoButton albumId={id_album} />
          </Box>
        </Box>
        <PhotosGrid id_album={id_album} />
      </Box>
    </PageWrapper>
  );
}

export default Albums;

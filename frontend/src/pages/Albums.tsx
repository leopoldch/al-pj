import React from "react";
import { Box } from "@mui/material";

import PageWrapper from "../components/PageWrapper";
import AlbumsGrid from "../components/AlbumsGrid";
import AlbumManagement from "../components/AlbumManagement";

function Albums() {
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
        <AlbumManagement />
        <AlbumsGrid />
      </Box>
    </PageWrapper>
  );
}

export default Albums;

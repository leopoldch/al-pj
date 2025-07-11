// footer

import React from "react";
import { Box, Typography } from "@mui/material";
import { mainFontColor } from "../utils/constants";
function Footer() {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "30px",
        position: "relative",
        marginTop: "auto",
        width: "100%",
        backgroundColor: "transparent",
      }}
    >
      <Typography variant="body1" color={mainFontColor}>
        © 2025 Aurianne Schwartz & Léopold Chappuis
      </Typography>
    </Box>
  );
}
export default Footer;

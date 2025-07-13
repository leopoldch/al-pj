import { Box, useMediaQuery, useTheme } from "@mui/material";
import React from "react";
import { mainFontColor } from "../utils/constants";
import { useNavigate } from "react-router-dom";
import OptionsButton from "./OptionsButton";
import PresenceIndicator from "./PresenceIndicator";

function Header() {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile: boolean = useMediaQuery(theme.breakpoints.down("md"));

  function handleClick() {
    navigate("/");
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: isMobile ? "column-reverse" : "row",
        justifyContent: isMobile ? "center" : "space-between",
        alignItems: "center",
        height: isMobile ? "auto" : "100px",
        paddingLeft: isMobile ? "10px" : "20px",
        paddingRight: isMobile ? "10px" : "20px",
        gap: isMobile ? "10px" : "20px",
        paddingTop: isMobile ? "10px" : "5px",
        paddingBottom: isMobile ? "10px" : 0,
        marginBottom: isMobile ? "0px" : "100px",
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: isMobile ? "column" : "row",
          alignItems: "center",
          gap: isMobile ? "5px" : "20px",
        }}
      >
        <Box
          onClick={handleClick}
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            cursor: "pointer",
          }}
        >
          <img
            src="./icon.png"
            alt="Logo"
            style={{
              width: isMobile ? "70px" : "100px",
              height: isMobile ? "70px" : "100px",
              borderRadius: "10px",
            }}
          />
        </Box>

        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <h1
            style={{
              color: mainFontColor,
              fontWeight: "bold",
              fontSize: isMobile ? "24px" : "40px",
              margin: 0,
            }}
          >
            Aurianne et Léo
          </h1>
        </Box>
      </Box>

      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          gap: isMobile ? "20px" : "100px",
          alignItems: "center",
          justifyContent: isMobile ? "space-between" : "unset",
          width: isMobile ? "100%" : "auto",
        }}
      >
        <PresenceIndicator />
        <OptionsButton />
      </Box>
    </Box>
  );
}

export default Header;

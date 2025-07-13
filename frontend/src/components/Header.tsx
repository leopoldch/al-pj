import { Box } from "@mui/material";
import React from "react";
import { mainFontColor } from "../utils/constants";
import { useNavigate } from "react-router-dom";
import OptionsButton from "./OptionsButton";
import PresenceIndicator from "./PresenceIndicator";

function Header() {
  const navigate = useNavigate();
  function handleClick() {
    navigate("/");
  }

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        height: "100px",
        paddingLeft: "20px",
        paddingRight: "20px",
        gap: "20px",
        paddingTop: "5px",
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          gap: "20px",
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
            style={{ width: "100px", height: "100px", borderRadius: "10px" }}
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
              fontSize: "40px",
            }}
          >
            Aurianne et Léo
          </h1>
        </Box>
      </Box>
      <Box sx={{ display: "flex", flexDirection: "row", gap: "100px", alignItems: "center" }}>
        <PresenceIndicator />
        <OptionsButton />
      </Box>
    </Box>
  );
}

export default Header;

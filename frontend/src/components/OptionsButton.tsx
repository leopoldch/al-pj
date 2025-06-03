import React from "react";
import { Box, Button, Menu, MenuItem, Typography } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import LogoutIcon from "@mui/icons-material/Logout";
import ChecklistIcon from "@mui/icons-material/Checklist";
import HouseIcon from "@mui/icons-material/House";
import { useLocation, useNavigate } from "react-router-dom";

export default function OptionsButton() {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const location = useLocation();

  const isHomePage = location.pathname === "/";

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    navigate("/login");
  };

  function handleOptionClick(arg: string): void {
    navigate(`/${arg}`);
  }

  return (
    <div>
      <Button
        aria-controls="options-menu"
        aria-haspopup="true"
        onClick={handleClick}
        variant="contained"
      >
        <MenuIcon />
      </Button>
      <Menu id="options-menu" anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        {!isHomePage && (
          <MenuItem onClick={() => handleOptionClick("")}>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                width: "140px",
              }}
            >
              <Typography>Home</Typography>
              <HouseIcon />
            </Box>
          </MenuItem>
        )}
        <MenuItem onClick={() => handleOptionClick("bucketpoints")}>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              width: "140px",
            }}
          >
            <Typography>BucketsPoints</Typography>
            <ChecklistIcon />
          </Box>
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              width: "140px",
            }}
          >
            <Typography>Déconnexion</Typography>
            <LogoutIcon />
          </Box>
        </MenuItem>
      </Menu>
    </div>
  );
}

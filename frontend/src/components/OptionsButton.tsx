import React from "react";
import { Box, Button, Menu, MenuItem, Typography } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import LogoutIcon from "@mui/icons-material/Logout";
import { useNavigate } from "react-router-dom";

export default function OptionsButton() {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

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
        {/*<MenuItem onClick={() => handleOptionClick('photos')}><PhotoCameraIcon/></MenuItem>*/}
        <MenuItem onClick={handleLogout}>
          {
            <Box sx={{ display: "flex", alignContent: "center", gap: "5px" }}>
              <Typography>Déconnection</Typography> <LogoutIcon />
            </Box>
          }
        </MenuItem>
      </Menu>
    </div>
  );
}

import React, { useState } from "react";
import { Box, Modal, TextField, Button, IconButton } from "@mui/material";
import LockIcon from "@mui/icons-material/Lock";
import BridgeImg from "../assets/bridge.png";

function BridgeDisplay() {
  const [locks, setLocks] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [clickPosition, setClickPosition] = useState({ x: 0, y: 0 });
  const [lockDetails, setLockDetails] = useState({ name: "" });

  const handleBridgeClick = (e: { currentTarget: { getBoundingClientRect: () => any; }; clientX: number; clientY: number; }) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    setClickPosition({ x, y });
    setModalOpen(true);
  };

  const handleAddLock = () => {
    console.log("Adding lock at:", clickPosition, "with name:", lockDetails.name);
  };

  return (
    <Box sx={{ position: "relative", width: "800px", margin: "auto" }}>
      <Box
        component="img"
        src={BridgeImg}
        alt="Bridge"
        sx={{ width: "100%", cursor: "crosshair", borderRadius: 5 }}
        onClick={handleBridgeClick}
      />

      <Modal open={modalOpen} onClose={() => setModalOpen(false)}>
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            background: "#fff",
            padding: 3,
            borderRadius: 2,
            width: 300,
          }}
        >
          <h3>Add a Lock</h3>
          <TextField
            label="Lock Name"
            fullWidth
            value={lockDetails.name}
            onChange={(e) => setLockDetails({ name: e.target.value })}
            sx={{ mb: 2 }}
          />
          <Button variant="contained" fullWidth onClick={handleAddLock}>
            Add Lock
          </Button>
        </Box>
      </Modal>
    </Box>
  );
}

export default BridgeDisplay;

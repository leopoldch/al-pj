import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItemText,
  Stack,
  IconButton,
  Checkbox,
  Paper,
  Typography,
  InputBase,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import {
  useBucketPointsQuery,
  useDeleteBucketPointMutation,
  useUpdateBucketPointMutation,
} from "../queries/bucketpoints";
import IBucketPoint from "../types/bucketspoints";
import BucketPointsInput from "./BucketPointsInput";
import { useWebSocketContext } from "../contexts/WebSocketProvider";
import { WebSocketMessageType } from "../types/websockets";
import {
  BucketPointCreated,
  BucketPointDeleted,
  BucketPointUpdated,
} from "../types/websocket-interfaces";

export default function BucketPointsDisplay() {
  const { data: bucketPointsList, isLoading } = useBucketPointsQuery();
  const [bucketPoints, setBucketPoints] = useState<IBucketPoint[]>(bucketPointsList || []);
  const deleteBucketPoint = useDeleteBucketPointMutation();
  const updateBucketPoint = useUpdateBucketPointMutation();
  const websocket = useWebSocketContext();

  const [openModal, setOpenModal] = useState(false);
  const [currentBucketPoint, setCurrentBucketPoint] = useState<IBucketPoint | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [search, setSearch] = useState("");

  const theme = useTheme();
  const isMobile: boolean = useMediaQuery(theme.breakpoints.down("md"));

  const handleDelete = (id: number) => {
    deleteBucketPoint.mutate(id);
  };

  const handleToggleCompleted = (bucketPoint: IBucketPoint) => {
    updateBucketPoint.mutate({
      id: bucketPoint.id,
      data: { completed: !bucketPoint.completed },
    });
  };

  const handleEditOpen = (bucketPoint: IBucketPoint) => {
    setCurrentBucketPoint(bucketPoint);
    setEditTitle(bucketPoint.title);
    setEditDescription(bucketPoint.description);
    setOpenModal(true);
  };

  const handleEditSave = () => {
    if (currentBucketPoint) {
      updateBucketPoint.mutate({
        id: currentBucketPoint.id,
        data: { title: editTitle, description: editDescription },
      });
    }
    setOpenModal(false);
  };

  useEffect(() => {
    const handleDeleteBucketPoint = (data: BucketPointDeleted) => {
      setBucketPoints((prev) => prev.filter((bp) => bp.id !== data.id));
    };

    const handleNewBucketPoint = (data: BucketPointCreated) => {
      console.debug("New bucket point received:", data);
      const bp = data.data;
      setBucketPoints((prev) => [bp, ...prev]);
    };

    const handleUpdateBucketPoint = (data: BucketPointUpdated) => {
      console.debug("Bucket point updated:", data);
      const updatedPoint = data.data;
      setBucketPoints((prev) =>
        prev.map((bp) => (bp.id === updatedPoint.id ? { ...bp, ...updatedPoint } : bp))
      );
    };

    websocket.bind(WebSocketMessageType.BucketPointCreated, handleNewBucketPoint);
    websocket.bind(WebSocketMessageType.BucketPointDeleted, handleDeleteBucketPoint);
    websocket.bind(WebSocketMessageType.BucketPointUpdated, handleUpdateBucketPoint);

    return () => {
      websocket.unbind(WebSocketMessageType.BucketPointCreated, handleNewBucketPoint);
      websocket.unbind(WebSocketMessageType.BucketPointDeleted, handleDeleteBucketPoint);
      websocket.unbind(WebSocketMessageType.BucketPointUpdated, handleUpdateBucketPoint);
    };
  }, [websocket]);

  useEffect(() => {
    if (bucketPointsList) {
      setBucketPoints(bucketPointsList);
    }
  }, [bucketPointsList]);

  if (isLoading) {
    return <Box>Loading...</Box>;
  }

  const completedCount = bucketPoints?.filter((point) => point.completed).length || 0;

  const filteredBucketPoints =
    bucketPoints
      ?.filter(
        (point) =>
          point.title.toLowerCase().includes(search.toLowerCase()) ||
          point.description.toLowerCase().includes(search.toLowerCase())
      )
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()) || [];

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      mt={-2}
      width={isMobile ? "95%" : "60%"}
      height="auto"
    >
      <Box
        display="flex"
        flexDirection={isMobile ? "column" : "row"}
        justifyContent="space-between"
        alignItems={isMobile ? "flex-start" : "center"}
        width="100%"
        mb={2}
        gap={isMobile ? 2 : 0}
      >
        <Box
          sx={{
            display: "flex",
            flexDirection: isMobile ? "column" : "row",
            alignItems: isMobile ? "flex-start" : "center",
            gap: isMobile ? "8px" : "10px",
          }}
        >
          <Typography variant={isMobile ? "h5" : "h4"}>À faire ensemble 🧸</Typography>
          <BucketPointsInput />
        </Box>

        <Box
          display="flex"
          flexDirection={isMobile ? "column" : "row"}
          alignItems={isMobile ? "flex-start" : "center"}
          gap={isMobile ? 1 : 2}
          width={isMobile ? "100%" : "auto"}
        >
          <Typography variant="h6" color="text.secondary">
            {completedCount} réalisés
          </Typography>
          <InputBase
            placeholder="Rechercher..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            sx={{
              p: 1,
              border: "1px solid #ccc",
              borderRadius: 2,
              backgroundColor: "rgba(255,255,255,0.9)",
              width: isMobile ? "100%" : "auto",
            }}
          />
        </Box>
      </Box>

      <List
        sx={{
          width: "100%",
          height: isMobile ? "45vh" : "60vh",
          overflowY: "auto",
          pr: 1,
        }}
      >
        {filteredBucketPoints.map((bucketPoint) => (
          <Paper
            key={bucketPoint.id}
            elevation={3}
            sx={{
              mb: 2,
              p: isMobile ? 1 : 2,
              backgroundColor: "rgba(255, 255, 255, 0.8)",
              borderRadius: 2,
            }}
          >
            <Stack
              direction={isMobile ? "column" : "row"}
              alignItems={isMobile ? "flex-start" : "center"}
              spacing={isMobile ? 1 : 2}
            >
              <Checkbox
                checked={bucketPoint.completed}
                onChange={() => handleToggleCompleted(bucketPoint)}
              />
              <Box flexGrow={1}>
                <ListItemText
                  primary={
                    <Typography
                      variant="h6"
                      sx={{
                        fontSize: isMobile ? "1rem" : "1.2rem",
                        textDecoration: bucketPoint.completed ? "line-through" : "none",
                        wordBreak: "break-word",
                      }}
                    >
                      {bucketPoint.title}
                    </Typography>
                  }
                  secondary={
                    <>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ wordBreak: "break-word" }}
                      >
                        Description: {bucketPoint.description}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Ajouté le : {new Date(bucketPoint.created_at).toLocaleDateString()}
                      </Typography>
                    </>
                  }
                />
              </Box>
              <Stack direction="row" spacing={1} mt={isMobile ? 1 : 0}>
                <IconButton color="primary" onClick={() => handleEditOpen(bucketPoint)}>
                  <EditIcon fontSize={isMobile ? "small" : "medium"} />
                </IconButton>
                <IconButton color="error" onClick={() => handleDelete(bucketPoint.id)}>
                  <DeleteIcon fontSize={isMobile ? "small" : "medium"} />
                </IconButton>
              </Stack>
            </Stack>
          </Paper>
        ))}
      </List>

      <Dialog open={openModal} onClose={() => setOpenModal(false)} fullWidth={isMobile}>
        <DialogTitle>Modifier le Bucket Point</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            <TextField
              label="Titre"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              fullWidth
            />
            <TextField
              label="Description"
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenModal(false)}>Annuler</Button>
          <Button variant="contained" onClick={handleEditSave}>
            Sauvegarder
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

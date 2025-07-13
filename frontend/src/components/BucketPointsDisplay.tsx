import React, { useState } from "react";
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

export default function BucketPointsDisplay() {
  const { data: bucketPoints, isLoading } = useBucketPointsQuery();
  const deleteBucketPoint = useDeleteBucketPointMutation();
  const updateBucketPoint = useUpdateBucketPointMutation();

  const [openModal, setOpenModal] = useState(false);
  const [currentBucketPoint, setCurrentBucketPoint] = useState<IBucketPoint | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [search, setSearch] = useState("");

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

  if (isLoading) {
    return <Box>Loading...</Box>;
  }

  const completedCount = bucketPoints?.filter((point) => point.completed).length || 0;

  // filtrage dynamique selon le champ search
  const filteredBucketPoints =
    bucketPoints
      ?.filter(
        (point) =>
          point.title.toLowerCase().includes(search.toLowerCase()) ||
          point.description.toLowerCase().includes(search.toLowerCase())
      )
      .sort(
        (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      ) || [];

  return (
    <Box display="flex" flexDirection="column" alignItems="center" mt={4} width="60%">
      <Box display="flex" justifyContent="space-between" alignItems="center" width="100%" mb={2}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "row",
            alignContent: "center",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <Typography variant="h4">À faire ensemble 🧸</Typography>
          <BucketPointsInput />
        </Box>
        <Box display="flex" alignItems="center" gap={2}>
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
            }}
          />
        </Box>
      </Box>

      <List
        sx={{
          width: "100%",
          height: "70vh",
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
              p: 2,
              backgroundColor: "rgba(255, 255, 255, 0.8)",
              borderRadius: 2,
            }}
          >
            <Stack direction="row" alignItems="center" spacing={2}>
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
                        textDecoration: bucketPoint.completed ? "line-through" : "none",
                      }}
                    >
                      {bucketPoint.title}
                    </Typography>
                  }
                  secondary={
                    <>
                      <Typography variant="body2" color="text.secondary">
                        Description: {bucketPoint.description}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Ajouté le : {new Date(bucketPoint.created_at).toLocaleDateString()}
                      </Typography>
                    </>
                  }
                />
              </Box>
              <Stack direction="row" spacing={1}>
                <IconButton color="primary" onClick={() => handleEditOpen(bucketPoint)}>
                  <EditIcon />
                </IconButton>
                <IconButton color="error" onClick={() => handleDelete(bucketPoint.id)}>
                  <DeleteIcon />
                </IconButton>
              </Stack>
            </Stack>
          </Paper>
        ))}
      </List>

      <Dialog open={openModal} onClose={() => setOpenModal(false)}>
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

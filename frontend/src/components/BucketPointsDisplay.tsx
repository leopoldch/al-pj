import React, { useEffect, useState } from "react"
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
    ToggleButtonGroup,
    ToggleButton,
    InputAdornment,
    useTheme,
    useMediaQuery,
    Chip,
} from "@mui/material"
import DeleteIcon from "@mui/icons-material/Delete"
import EditIcon from "@mui/icons-material/Edit"
import SearchRounded from "@mui/icons-material/SearchRounded"
import {
    useBucketPointsQuery,
    useDeleteBucketPointMutation,
    useUpdateBucketPointMutation,
} from "../queries/bucketpoints"
import IBucketPoint from "../types/bucketspoints"
import BucketPointsInput from "./BucketPointsInput"
import { useWebSocketContext } from "../contexts/WebSocketProvider"
import { WebSocketMessageType } from "../types/websockets"
import {
    BucketPointCreated,
    BucketPointDeleted,
    BucketPointUpdated,
} from "../types/websocket-interfaces"

export default function BucketPointsDisplay() {
    const { data: bucketPointsList, isLoading } = useBucketPointsQuery()
    const [bucketPoints, setBucketPoints] = useState<IBucketPoint[]>(bucketPointsList || [])
    const deleteBucketPoint = useDeleteBucketPointMutation()
    const updateBucketPoint = useUpdateBucketPointMutation()
    const websocket = useWebSocketContext()

    const [openModal, setOpenModal] = useState(false)
    const [currentBucketPoint, setCurrentBucketPoint] = useState<IBucketPoint | null>(null)
    const [editTitle, setEditTitle] = useState("")
    const [editDescription, setEditDescription] = useState("")
    const [search, setSearch] = useState("")
    const [maskCompleted, setMaskCompleted] = useState<boolean>(false)

    const theme = useTheme()
    const isMobile: boolean = useMediaQuery(theme.breakpoints.down("md"))

    const handleDelete = (id: number) => {
        deleteBucketPoint.mutate(id)
    }

    const handleToggleCompleted = (bucketPoint: IBucketPoint) => {
        updateBucketPoint.mutate({
            id: bucketPoint.id,
            data: { completed: !bucketPoint.completed },
        })
    }

    const handleEditOpen = (bucketPoint: IBucketPoint) => {
        setCurrentBucketPoint(bucketPoint)
        setEditTitle(bucketPoint.title)
        setEditDescription(bucketPoint.description)
        setOpenModal(true)
    }

    const handleEditSave = () => {
        if (currentBucketPoint) {
            updateBucketPoint.mutate({
                id: currentBucketPoint.id,
                data: { title: editTitle, description: editDescription },
            })
        }
        setOpenModal(false)
    }

    useEffect(() => {
        const handleDeleteBucketPoint = (data: BucketPointDeleted) => {
            setBucketPoints((prev) => prev.filter((bp) => bp.id !== data.id))
        }

        const handleNewBucketPoint = (data: BucketPointCreated) => {
            console.debug("New bucket point received:", data)
            const bp = data.data
            setBucketPoints((prev) => [bp, ...prev])
        }

        const handleUpdateBucketPoint = (data: BucketPointUpdated) => {
            console.debug("Bucket point updated:", data)
            const updatedPoint = data.data
            setBucketPoints((prev) =>
                prev.map((bp) => (bp.id === updatedPoint.id ? { ...bp, ...updatedPoint } : bp))
            )
        }

        websocket.bind(WebSocketMessageType.BucketPointCreated, handleNewBucketPoint)
        websocket.bind(WebSocketMessageType.BucketPointDeleted, handleDeleteBucketPoint)
        websocket.bind(WebSocketMessageType.BucketPointUpdated, handleUpdateBucketPoint)

        return () => {
            websocket.unbind(WebSocketMessageType.BucketPointCreated, handleNewBucketPoint)
            websocket.unbind(WebSocketMessageType.BucketPointDeleted, handleDeleteBucketPoint)
            websocket.unbind(WebSocketMessageType.BucketPointUpdated, handleUpdateBucketPoint)
        }
    }, [websocket])

    useEffect(() => {
        if (bucketPointsList) {
            setBucketPoints(bucketPointsList)
        }
    }, [bucketPointsList])

    if (isLoading) {
        return <Box>Loading...</Box>
    }

    const completedCount = bucketPoints?.filter((point) => point.completed).length || 0

    let filteredBucketPoints =
        bucketPoints
            ?.filter(
                (point) =>
                    point.title.toLowerCase().includes(search.toLowerCase()) ||
                    point.description.toLowerCase().includes(search.toLowerCase())
            )
            .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()) ||
        []

    if (maskCompleted) {
        filteredBucketPoints = filteredBucketPoints.filter((point) => !point.completed)
    }

    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            mt={-2}
            width={isMobile ? "95%" : "60%"}
            height="auto"
        >
            <Paper
                elevation={0}
                sx={{
                    width: "100%",
                    px: isMobile ? 2 : 3,
                    py: isMobile ? 2 : 2.5,
                    mb: 2,
                    borderRadius: 3,
                    backdropFilter: "blur(8px)",
                    background: "rgba(255,255,255,0.45)",
                    border: "1px solid rgba(255,255,255,0.6)",
                    boxShadow: "0 10px 30px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.4)",
                }}
            >
                <Stack
                    direction={isMobile ? "column" : "row"}
                    alignItems={isMobile ? "stretch" : "center"}
                    justifyContent="space-between"
                    spacing={isMobile ? 2 : 3}
                    flexWrap="wrap"
                    useFlexGap
                >
                    <Stack
                        direction={isMobile ? "column" : "row"}
                        spacing={1.5}
                        alignItems={isMobile ? "flex-start" : "center"}
                        flexShrink={0}
                    >
                        <Typography
                            variant={isMobile ? "h5" : "h4"}
                            sx={{
                                lineHeight: 1.1,
                                letterSpacing: 0.2,
                                textShadow: "0 1px 0 rgba(255,255,255,0.6)",
                            }}
                        >
                            À faire ensemble 🧸
                        </Typography>

                        <Box sx={{ mt: isMobile ? 0.5 : 0 }}>
                            <BucketPointsInput />
                        </Box>
                    </Stack>

                    <Stack
                        direction={isMobile ? "column" : "row"}
                        spacing={isMobile ? 1.25 : 1.5}
                        alignItems={isMobile ? "stretch" : "center"}
                        sx={{ width: isMobile ? "100%" : "auto" }}
                    >
                        <Chip
                            label={`${completedCount} réalisés`}
                            variant="outlined"
                            icon={<span style={{ fontSize: 10, marginLeft: 4 }}>✓</span>}
                            sx={{
                                height: 36,
                                borderRadius: 2,
                                px: 1,
                                fontWeight: 600,
                                bgcolor: "rgba(255,255,255,0.6)",
                                borderColor: "rgba(0,0,0,0.06)",
                            }}
                        />

                        <ToggleButtonGroup
                            value={maskCompleted ? "hide" : "show"}
                            exclusive
                            onChange={(_, v) => {
                                if (v === "hide") setMaskCompleted(true)
                                if (v === "show") setMaskCompleted(false)
                            }}
                            size="small"
                            sx={{
                                bgcolor: "rgba(255,255,255,0.6)",
                                borderRadius: 2,
                                border: "1px solid rgba(0,0,0,0.06)",
                                "& .MuiToggleButton-root": {
                                    px: 1.5,
                                    py: 0.75,
                                    textTransform: "none",
                                    fontWeight: 600,
                                    "&.Mui-selected": {
                                        bgcolor: "primary.main",
                                        color: "primary.contrastText",
                                        "&:hover": { bgcolor: "primary.main" },
                                    },
                                },
                            }}
                        >
                            <ToggleButton value="show">Tout</ToggleButton>
                            <ToggleButton value="hide">Actifs</ToggleButton>
                        </ToggleButtonGroup>

                        <TextField
                            placeholder="Rechercher…"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            size="small"
                            fullWidth={isMobile}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <SearchRounded />
                                    </InputAdornment>
                                ),
                            }}
                            sx={{
                                minWidth: isMobile ? "100%" : 260,
                                "& .MuiOutlinedInput-root": {
                                    height: 36,
                                    borderRadius: 2,
                                    bgcolor: "rgba(255,255,255,0.9)",
                                },
                            }}
                        />
                    </Stack>
                </Stack>
            </Paper>

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
                                                textDecoration: bucketPoint.completed
                                                    ? "line-through"
                                                    : "none",
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
                                                Ajouté le :{" "}
                                                {new Date(
                                                    bucketPoint.created_at
                                                ).toLocaleDateString()}
                                            </Typography>
                                        </>
                                    }
                                />
                            </Box>
                            <Stack direction="row" spacing={1} mt={isMobile ? 1 : 0}>
                                <IconButton
                                    color="primary"
                                    onClick={() => handleEditOpen(bucketPoint)}
                                >
                                    <EditIcon fontSize={isMobile ? "small" : "medium"} />
                                </IconButton>
                                <IconButton
                                    color="error"
                                    onClick={() => handleDelete(bucketPoint.id)}
                                >
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
    )
}

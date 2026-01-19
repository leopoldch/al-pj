import React, { useState } from "react"
import {
    Card,
    CardMedia,
    Typography,
    Box,
    Stack,
    Modal,
    Backdrop,
    IconButton,
    CircularProgress,
    Tooltip,
    Zoom,
} from "@mui/material"
import LocationOnIcon from "@mui/icons-material/LocationOn"
import InsertPhotoIcon from "@mui/icons-material/InsertPhoto"
import DeleteIcon from "@mui/icons-material/Delete"
import { Photo } from "../types/photo"
import { useDeletePhotoMutation } from "../queries/photos"

interface PhotoCardProps {
    photo: Photo
    albumId: string
}

const PhotoCard = ({ photo, albumId }: PhotoCardProps) => {
    const [open, setOpen] = useState(false)
    const [isHovered, setIsHovered] = useState(false)
    const [confirmDelete, setConfirmDelete] = useState(false)
    const deletePhotoMutation = useDeletePhotoMutation()

    const handleOpen = () => setOpen(true)
    const handleClose = () => {
        setOpen(false)
        setConfirmDelete(false)
    }

    const handleDelete = (e: React.MouseEvent) => {
        e.stopPropagation()
        if (!confirmDelete) {
            setConfirmDelete(true)
            // Reset confirmation after 3 seconds
            setTimeout(() => setConfirmDelete(false), 3000)
            return
        }
        deletePhotoMutation.mutate({ albumId, photoId: photo.id })
    }

    const isDeleting = deletePhotoMutation.isPending

    return (
        <>
            <Card
                sx={{
                    width: 240,
                    height: 240,
                    position: "relative",
                    borderRadius: 2,
                    boxShadow: 3,
                    overflow: "hidden",
                    backgroundColor: "white",
                    cursor: "pointer",
                    transition: "transform 0.2s, box-shadow 0.2s",
                    "&:hover": {
                        transform: "scale(1.02)",
                        boxShadow: 6,
                    },
                }}
                onClick={handleOpen}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => {
                    setIsHovered(false)
                    setConfirmDelete(false)
                }}
            >
                {photo.image_url ? (
                    <CardMedia
                        component="img"
                        image={photo.image_url}
                        alt={photo.caption || "Photo"}
                        sx={{
                            width: "100%",
                            height: "100%",
                            objectFit: "cover",
                            opacity: isDeleting ? 0.5 : 1,
                            transition: "opacity 0.3s",
                        }}
                    />
                ) : (
                    <Box
                        sx={{
                            height: "100%",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            backgroundColor: "#f0f0f0",
                        }}
                    >
                        <InsertPhotoIcon sx={{ fontSize: 48, color: "#bdbdbd" }} />
                    </Box>
                )}

                {/* Delete button - visible on hover */}
                <Zoom in={isHovered && !isDeleting}>
                    <Tooltip title={confirmDelete ? "Cliquer pour confirmer" : "Supprimer"}>
                        <IconButton
                            onClick={handleDelete}
                            sx={{
                                position: "absolute",
                                top: 8,
                                right: 8,
                                backgroundColor: confirmDelete ? "error.main" : "rgba(0,0,0,0.5)",
                                color: "white",
                                "&:hover": {
                                    backgroundColor: confirmDelete
                                        ? "error.dark"
                                        : "rgba(0,0,0,0.7)",
                                },
                            }}
                            size="small"
                        >
                            <DeleteIcon fontSize="small" />
                        </IconButton>
                    </Tooltip>
                </Zoom>

                {/* Loading indicator when deleting */}
                {isDeleting && (
                    <Box
                        sx={{
                            position: "absolute",
                            top: "50%",
                            left: "50%",
                            transform: "translate(-50%, -50%)",
                        }}
                    >
                        <CircularProgress size={40} />
                    </Box>
                )}

                <Box
                    sx={{
                        position: "absolute",
                        bottom: 0,
                        left: 0,
                        width: "100%",
                        px: 1,
                        pb: 0.5,
                        background: "linear-gradient(to top, rgba(0,0,0,0.5), rgba(0,0,0,0))",
                    }}
                >
                    <Stack spacing={0.3}>
                        {photo.caption && (
                            <Box
                                sx={{
                                    backgroundColor: "rgba(48, 48, 48, 0.5)",
                                    borderRadius: 1,
                                    px: 0.5,
                                    py: 0.1,
                                    width: "fit-content",
                                }}
                            >
                                <Typography variant="caption" color="white" noWrap>
                                    {photo.caption}
                                </Typography>
                            </Box>
                        )}
                        {photo.location && (
                            <Box
                                sx={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 0.5,
                                    backgroundColor: "rgba(48, 48, 48, 0.5)",
                                    borderRadius: 1,
                                    px: 0.5,
                                    py: 0.1,
                                    width: "fit-content",
                                }}
                            >
                                <LocationOnIcon fontSize="small" sx={{ color: "white" }} />
                                <Typography variant="caption" color="white" noWrap>
                                    {photo.location}
                                </Typography>
                            </Box>
                        )}
                        <Box
                            sx={{
                                backgroundColor: "rgba(48, 48, 48, 0.5)",
                                borderRadius: 1,
                                px: 0.5,
                                py: 0.1,
                                width: "fit-content",
                            }}
                        >
                            <Typography variant="caption" color="white" noWrap>
                                {new Date(photo.created_at).toLocaleDateString("fr-FR")}
                            </Typography>
                        </Box>
                    </Stack>
                </Box>
            </Card>

            <Modal
                open={open}
                onClose={handleClose}
                closeAfterTransition
                slots={{ backdrop: Backdrop }}
                slotProps={{
                    backdrop: {
                        timeout: 300,
                        sx: { backgroundColor: "rgba(0,0,0,0.7)" },
                    },
                }}
            >
                <Box
                    sx={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100vw",
                        height: "100vh",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        p: 2,
                        boxSizing: "border-box",
                    }}
                >
                    <Box
                        sx={{
                            position: "fixed",
                            top: 16,
                            right: 16,
                            display: "flex",
                            gap: 1,
                            zIndex: 1301,
                        }}
                    >
                        {/* Delete button in modal */}
                        <Tooltip title={confirmDelete ? "Cliquer pour confirmer" : "Supprimer"}>
                            <Box
                                onClick={handleDelete}
                                sx={{
                                    backgroundColor: confirmDelete
                                        ? "rgba(211,47,47,0.8)"
                                        : "rgba(0,0,0,0.6)",
                                    borderRadius: "50%",
                                    width: 36,
                                    height: 36,
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    cursor: isDeleting ? "wait" : "pointer",
                                    transition: "background-color 0.2s",
                                    "&:hover": {
                                        backgroundColor: confirmDelete
                                            ? "rgba(198,40,40,0.9)"
                                            : "rgba(0,0,0,0.8)",
                                    },
                                }}
                            >
                                {isDeleting ? (
                                    <CircularProgress size={16} sx={{ color: "white" }} />
                                ) : (
                                    <DeleteIcon sx={{ color: "white", fontSize: 18 }} />
                                )}
                            </Box>
                        </Tooltip>

                        {/* Download button */}
                        <Box
                            component="a"
                            href={photo.image_url}
                            download
                            sx={{
                                backgroundColor: "rgba(0,0,0,0.6)",
                                borderRadius: "50%",
                                width: 36,
                                height: 36,
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                cursor: "pointer",
                                textDecoration: "none",
                            }}
                        >
                            <Typography color="white" fontWeight="bold" fontSize={16}>
                                ↓
                            </Typography>
                        </Box>

                        {/* Close button */}
                        <Box
                            onClick={handleClose}
                            sx={{
                                backgroundColor: "rgba(0,0,0,0.6)",
                                borderRadius: "50%",
                                width: 36,
                                height: 36,
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                cursor: "pointer",
                            }}
                        >
                            <Typography color="white" fontWeight="bold" fontSize={20}>
                                ×
                            </Typography>
                        </Box>
                    </Box>

                    <Box
                        sx={{
                            maxWidth: { xs: "95vw", sm: "90vw", md: "70vw" },
                            maxHeight: { xs: "90vh", sm: "85vh", md: "80vh" },
                            display: "flex",
                            flexDirection: "column",
                            borderRadius: 2,
                            overflow: "hidden",
                            boxShadow: 5,
                            backgroundColor: "#1e1e1e",
                        }}
                    >
                        <Box
                            component="img"
                            src={photo.image_url}
                            alt={photo.caption || "Photo"}
                            sx={{
                                width: "100%",
                                height: "auto",
                                objectFit: "contain",
                                maxHeight: "calc(80vh - 48px)",
                                backgroundColor: "black",
                            }}
                        />

                        <Box
                            sx={{
                                width: "100%",
                                backgroundColor: "rgba(0, 0, 0, 0.8)",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "space-between",
                                px: 2,
                                py: 1,
                                color: "white",
                                fontSize: 14,
                            }}
                        >
                            <Box
                                sx={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 2,
                                    flexWrap: "wrap",
                                }}
                            >
                                {photo.caption && (
                                    <Typography
                                        variant="body2"
                                        color="white"
                                        sx={{ whiteSpace: "nowrap" }}
                                    >
                                        {photo.caption}
                                    </Typography>
                                )}
                                {photo.location && (
                                    <Box display="flex" alignItems="center" gap={0.5}>
                                        <LocationOnIcon fontSize="small" sx={{ color: "white" }} />
                                        <Typography
                                            variant="body2"
                                            color="white"
                                            sx={{ whiteSpace: "nowrap" }}
                                        >
                                            {photo.location}
                                        </Typography>
                                    </Box>
                                )}
                            </Box>

                            <Typography
                                variant="caption"
                                color="white"
                                sx={{ whiteSpace: "nowrap" }}
                            >
                                {new Date(photo.created_at).toLocaleDateString("fr-FR")}
                            </Typography>
                        </Box>
                    </Box>
                </Box>
            </Modal>
        </>
    )
}

export default PhotoCard

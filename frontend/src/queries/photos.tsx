import { useMutation, UseMutationResult, useQuery, UseQueryResult } from "@tanstack/react-query"
import { useAuth } from "../hooks/useAuth"
import { Photo } from "../types/photo"
import { useQueryClient } from "@tanstack/react-query"
import { AddPhotoInput } from "../types/photo"

export function useGetPhotos(
    albumId: string
): UseQueryResult<{ photos: Photo[]; album_id: string }, unknown> {
    const { axiosInstance } = useAuth()

    return useQuery<{ photos: Photo[]; album_id: string }, unknown>({
        queryKey: ["photos", albumId],
        queryFn: async () => {
            const response = await axiosInstance.get(`/photos/${albumId}/`)
            return response.data
        },
        enabled: !!albumId,
    })
}

export const useAddPhotoMutation = (): UseMutationResult<Photo, unknown, AddPhotoInput> => {
    const { axiosInstance } = useAuth()
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async ({ albumId, image, caption, location }: AddPhotoInput) => {
            const formData = new FormData()

            if (image) {
                formData.append("image", image)
            }
            if (caption) {
                formData.append("caption", caption)
            }
            if (location) {
                formData.append("location", location)
            }

            const response = await axiosInstance.post(`/photos/${albumId}/`, formData)

            return response.data
        },

        onSuccess: (_data, { albumId }) => {
            queryClient.invalidateQueries({ queryKey: ["photos", albumId] })
        },
    })
}

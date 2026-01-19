import {
    useMutation,
    UseMutationResult,
    useQuery,
    UseQueryResult,
    useInfiniteQuery,
} from "@tanstack/react-query"
import Imessage, { PaginatedResponse } from "../types/messages"
import { useAuth } from "../hooks/useAuth"

const MESSAGE_QUERY_KEY = ["messages"]

const useGetAllMessages = (): UseQueryResult<Imessage[], unknown> => {
    const { axiosInstance } = useAuth()

    return useQuery<Imessage[], unknown>({
        queryKey: MESSAGE_QUERY_KEY,
        queryFn: async () => {
            const response = await axiosInstance.get<Imessage[]>("/messages/")
            return response.data
        },
    })
}

const usePostMessage = (): UseMutationResult<Imessage, unknown, string> => {
    const { axiosInstance } = useAuth()

    return useMutation<Imessage, unknown, string>({
        mutationFn: async (newMessage: string) => {
            const response = await axiosInstance.post("/messages/", {
                message: newMessage,
            })
            return response.data
        },
    })
}

const useDeleteMessage = (): UseMutationResult<void, unknown, number> => {
    const { axiosInstance } = useAuth()

    return useMutation<void, unknown, number>({
        mutationFn: async (id: number) => {
            await axiosInstance.delete<void>(`/messages/${id}/`)
        },
    })
}

const useGetPaginatedMessages = () => {
    const { axiosInstance } = useAuth()

    return useInfiniteQuery({
        initialPageParam: 1,
        queryKey: ["messages", "paginated"],
        queryFn: async ({ pageParam = 1 }) => {
            const response = await axiosInstance.get<PaginatedResponse<Imessage>>(
                `/messages/paginated/?page=${pageParam}`
            )
            return response.data
        },
        getNextPageParam: (lastPage) => {
            if (lastPage.next) {
                try {
                    const url = new URL(lastPage.next, window.location.origin)
                    const page = url.searchParams.get("page")
                    return page ? Number(page) : undefined
                } catch (e) {
                    console.error("Error parsing next page URL:", e)
                    return undefined
                }
            }
            return undefined
        },
    })
}

export { useGetAllMessages, usePostMessage, useDeleteMessage, useGetPaginatedMessages }

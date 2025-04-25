import {
  useMutation,
  UseMutationResult,
  useQuery,
  useQueryClient,
  UseQueryResult,
} from "@tanstack/react-query"
import Imessage from "../types/messages"
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
  const queryClient = useQueryClient()

  return useMutation<Imessage, unknown, string>({
    mutationFn: async (newMessage: string) => {
      const response = await axiosInstance.post("/messages/", {
        message: newMessage,
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MESSAGE_QUERY_KEY })
    },
  })
}

const useDeleteMessage = (): UseMutationResult<void, unknown, number> => {
  const { axiosInstance } = useAuth()
  const queryClient = useQueryClient()

  return useMutation<void, unknown, number>({
    mutationFn: async (id: number) => {
      await axiosInstance.delete<void>(`/messages/${id}/`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MESSAGE_QUERY_KEY })
    },
  })
}

export { useGetAllMessages, usePostMessage, useDeleteMessage }

import { useQuery, UseQueryResult } from "@tanstack/react-query"
import { useAuth } from "../hooks/useAuth"
import { IUserPresence } from "../types/user"

export const useGetPresence = (): UseQueryResult<IUserPresence, unknown> => {
    const { axiosInstance } = useAuth()

    return useQuery<IUserPresence, unknown>({
        queryKey: ["presence"],
        queryFn: async () => {
            const response = await axiosInstance.get("/presence/")
            return response.data
        },
    })
}

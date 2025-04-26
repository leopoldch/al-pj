import { useMutation, UseMutationResult } from "@tanstack/react-query"
import { useQuery, UseQueryResult } from "@tanstack/react-query"
import IUser from "../types/user"
import getBaseURL from "../utils/utils";

const apiUrl = getBaseURL() + "/api/";

interface LoginResponse {
  refresh: string
  access: string
}

interface LoginVariables {
  username: string
  password: string
}

export const useLogin = (): UseMutationResult<LoginResponse, Error, LoginVariables> => {
  return useMutation<LoginResponse, Error, LoginVariables>({
    mutationFn: async (variables: LoginVariables) => {
      const response = await fetch(apiUrl + "token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(variables),
      })

      if (!response.ok) {
        throw new Error("Failed to login")
      }

      const data = await response.json()
      localStorage.setItem("token", data.access)
      localStorage.setItem("refresh", data.refresh)

      return data
    },
  })
}

export const useGetProfile = (): UseQueryResult<IUser, Error> => {
  return useQuery<IUser, Error>({
    queryKey: ["profile"],
    queryFn: async () => {
      const token = localStorage.getItem("token")
      if (!token) {
        throw new Error("No token found")
      }

      const response = await fetch(apiUrl + "profile/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error("Failed to fetch profile")
      }

      return await response.json()
    },
  })
}

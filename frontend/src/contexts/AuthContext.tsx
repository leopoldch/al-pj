import React, { createContext, useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import axios, { AxiosInstance } from "axios";
import { HttpStatusCode } from "axios";
import { useGetProfile } from "../queries/auth";
import IUser from "../types/user";
import getBaseURL from "../utils/utils";

interface AuthContextType {
  user: IUser;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  axiosInstance: AxiosInstance;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<IUser | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("token"));
  const navigate = useNavigate();
  const { data: profile, isSuccess } = useGetProfile();

  const baseUrl =
    process.env.NODE_ENV === "development" ? process.env.REACT_APP_API_URL : getBaseURL() + "/api/";

  useEffect(() => {
    if (isSuccess && profile) {
      setUser(profile);
      console.log("Profile:", profile);
    }
  }, [isSuccess, profile]);

  useEffect(() => {
    if (!token) {
      logout();
      navigate("/login");
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await fetch(baseUrl + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error("Login failed");
    const { token } = await res.json();
    localStorage.setItem("token", token);
    setToken(token);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  const axiosInstance = useMemo(() => {
    if (!token) {
      return;
    }
    const instance = axios.create({
      baseURL: baseUrl,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    instance.interceptors.response.use(
      (res) => res,
      (e) => {
        switch (e.response?.status) {
          case HttpStatusCode.Unauthorized:
            logout();
            break;
        }
        throw e;
      }
    );
    return instance;
  }, [token, logout]);

  return (
    <AuthContext.Provider
      value={{
        user: user!,
        token,
        login,
        logout,
        isAuthenticated: !!token,
        axiosInstance: axiosInstance!,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

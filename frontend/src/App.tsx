import { Routes, Route, Outlet } from "react-router-dom";
import Home from "./pages/Home";
import { ThemeProvider, CssBaseline } from "@mui/material";
import { buildCustomTheme } from "./themes/Default";
import React from "react";
import Login from "./pages/Login";
import { AuthProvider } from "./contexts/AuthContext";
import BucketsPoints from "./pages/BucketPoints";
import WebSocketProvider from "./contexts/WebSocketProvider";
import Albums from "./pages/Albums";
import Photos from "./pages/Photos";

const theme = buildCustomTheme("light");

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route
          element={
            <AuthProvider>
              <WebSocketProvider>
                <Outlet />
              </WebSocketProvider>
            </AuthProvider>
          }
        >
          <Route path="/" element={<Home />} />
          <Route path="/bucketpoints" element={<BucketsPoints />} />
          <Route path="/albums" element={<Albums />} />
          <Route path="/photos/:id_album" element={<Photos />} />
        </Route>
        <Route path="/login" element={<Login />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;

// landing page for the app

import React from "react";
import { Box } from "@mui/material";

import Header from "../components/Header";
import Footer from "./Footer";

interface PageWrapperProps {
  children: React.ReactNode;
}

function PageWrapper({ children }: PageWrapperProps) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <Header />

      <Box sx={{ flexGrow: 1, display: "flex", flexDirection: "column", minHeight: 0 }}>
        {children}
      </Box>

      <Footer />
    </Box>
  );
}
export default PageWrapper;

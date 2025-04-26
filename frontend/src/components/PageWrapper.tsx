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
        minheight: "100%",
        backgroundImage: "url(./background.png)",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "repeat",
      }}
    >
      <Header />
      {children}
      <Footer />
    </Box>
  );
}
export default PageWrapper;

import React from "react";
import { Box, useMediaQuery, useTheme } from "@mui/material";

import PageWrapper from "../components/PageWrapper";
import MainInput from "../components/Input";
import DisplayAllMessages from "../components/DisplayMessages";

function Home() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  return (
    <PageWrapper>
      <Box
        sx={{
          flexGrow: 1,
          minHeight: 0, // important !
          display: "flex",
          flexDirection: "column",
          gap: theme.spacing(2),
          alignItems: "center",
          px: theme.spacing(2),
          py: theme.spacing(2),
        }}
      >
        {isMobile ? (
          <>
            <Box
              sx={{
                flexGrow: 1,
                minHeight: 0,
                width: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <DisplayAllMessages />
            </Box>
            <MainInput />
          </>
        ) : (
          <>
            <MainInput />
            <Box
              sx={{
                flexGrow: 1,
                minHeight: 0,
                width: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <DisplayAllMessages />
            </Box>
          </>
        )}
      </Box>
    </PageWrapper>
  );
}

export default Home;

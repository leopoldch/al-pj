// landing page for the app

import React from "react"
import { Box } from "@mui/material"

import PageWrapper from "../components/PageWrapper"
import MainInput from "../components/Input"
import DisplayAllMessages from "../components/DisplayMessages"

function Home() {
  return (
    <PageWrapper>
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          flexDirection: "column",
        }}
      >
        <MainInput />
        <DisplayAllMessages />
      </Box>
    </PageWrapper>
  )
}
export default Home

import React from "react";
import { Box } from "@mui/material";

import PageWrapper from "../components/PageWrapper";
import BucketPointsDisplay from "../components/BucketPointsDisplay";
import BucketPointsInput from "../components/BucketPointsInput";

function BucketsPoints() {
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
        <BucketPointsDisplay />
      </Box>
    </PageWrapper>
  );
}
export default BucketsPoints;

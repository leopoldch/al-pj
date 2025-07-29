import React from "react"
import { Box } from "@mui/material"

import PageWrapper from "../components/PageWrapper"
import BucketPointsDisplay from "../components/BucketPointsDisplay"

function BucketsPoints() {
    return (
        <PageWrapper>
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "flex-start",
                    gap: 2,
                    width: "100%",
                    px: 2,
                    py: 4,
                }}
            >
                <BucketPointsDisplay />
            </Box>
        </PageWrapper>
    )
}

export default BucketsPoints

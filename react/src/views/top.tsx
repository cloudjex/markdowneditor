import { Container, Tabs, Tab, Box } from "@mui/material";
import { useState } from "react";

import Header from "../components/header";
import Signin from "../components/signin";
import Signup from "../components/signup";

function Top() {
  const [tab, setTab] = useState(0);

  return (
    <>
      <title>Top</title>
      <Header />

      <Tabs
        value={tab}
        onChange={() => { setTab(tab === 0 ? 1 : 0); }}
        centered
        sx={{ marginTop: 3 }}
      >
        <Tab label="Sign In" />
        <Tab label="Sign Up" />
      </Tabs>

      <Container
        maxWidth="xs"
        sx={{
          marginTop: 3,
          border: "1px solid #ddd",
          borderRadius: "10px",
          padding: "15px",
        }}
      >

        <Box>
          {tab === 0 && <Signin />}
          {tab === 1 && <Signup />}
        </Box>

      </Container>
    </>
  );
};

export default Top;
import { Container, Tabs, Tab, Box } from "@mui/material";
import { useState } from "react";

import Signin from "@/src/components/auth/signin";
import Header from "@/src/components/header/header";


function Auth() {
  const [tab, setTab] = useState(0);

  return (
    <>
      <title>Top</title>
      <Header />

      <Tabs
        value={tab}
        onChange={() => { setTab(tab === 0 ? 1 : 0); }}
        centered
        sx={(theme) => ({
          marginTop: 3,

          [theme.breakpoints.down("sm")]: {
            marginTop: 5
          }
        })}
      >
        <Tab label="Sign In" />
      </Tabs >

      <Container
        maxWidth="xs"
        sx={(theme) => ({
          marginTop: 3,
          border: "1px solid #ddd",
          borderRadius: "10px",
          padding: "15px",

          [theme.breakpoints.down("sm")]: {
            marginTop: 5,
            width: "80%",
          },
        })}
      >

        <Box>
          {tab === 0 && <Signin />}
        </Box>

      </Container>
    </>
  );
};

export default Auth;

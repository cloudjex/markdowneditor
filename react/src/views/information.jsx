import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import Header from "../components/header";

function Information() {
  return (
    <>
      <title>Information</title>
      <Header />

      <Container maxWidth="xs" sx={{ marginTop: 10 }}>

        <Typography variant="h4" align="center">
          Information
        </Typography>

      </Container>
    </>
  );
};

export default Information;
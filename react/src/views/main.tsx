import { Container } from "@mui/material";

import Editor from "@/src/components/editor/editor";
import Header from "@/src/components/header/header";


function Main() {
  return (
    <>
      <title>Main</title>
      <Header />

      <Container sx={{ mt: 2 }}>
        <Editor />
      </Container>
    </>
  );
};

export default Main;
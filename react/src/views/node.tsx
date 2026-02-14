import { Container } from "@mui/material";
import { useParams } from "react-router-dom";

import Editor from "@/src/components/editor/editor";
import Header from "@/src/components/header/header";
import userStore from '@/src/store/user_store';


function Node() {
  const { tree } = userStore();
  const node_id = useParams<{ node_id: string }>().node_id || "";

  return (
    <>
      <title>Main</title>
      <Header tree={tree} node_id={node_id} />

      <Container sx={{ mt: 2 }}>
        <Editor tree={tree} node_id={node_id} />
      </Container>
    </>
  );
};

export default Node;

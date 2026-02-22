import { Container } from "@mui/material";
import { useParams } from "react-router-dom";

import Editor from "@/components/editor/editor";
import Header from "@/components/header/header";
import userStore from '@/store/user_store';


function Node() {
  const { tree } = userStore();
  const node_id = useParams<{ node_id: string }>().node_id || "";

  return (
    <>
      <title>Main</title>
      <Header tree={tree} nodeId={node_id} />

      <Container sx={{ mt: 2 }}>
        <Editor tree={tree} nodeId={node_id} />
      </Container>
    </>
  );
};

export default Node;

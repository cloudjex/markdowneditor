import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import { useEffect, useState } from 'react';

import Breadcrumb from "../components/breadcrumbs";
import EditerHeader from "../components/editer_header";
import Header from "../components/header";
import Loading from "../components/loading";
import MarkdownEditor from "../components/markdowneditor";
import userStore from "../store/user_store";
import utils from "../utils/utils";

import type { TreeNode } from "../types/types";

function Main() {
  const { id_token, setTree } = userStore();
  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const res_promise = utils.requests(
        `${import.meta.env.VITE_API_HOST}/trees`,
        "GET",
        { authorization: `Bearer ${id_token}` },
        {}
      );
      const res = await res_promise;

      const body = res.body as { tree: TreeNode };
      setTree(body.tree);
      setLoading(false);
    };

    if (id_token) {
      fetchData();
    };
  }, [id_token]);

  return (
    <>
      <title>Main</title>
      <Header />
      <Loading loading={isLoading} />

      <Container sx={{ mt: 2 }}>

        <Box display="flex" justifyContent="space-between">
          <Breadcrumb />
          <EditerHeader />
        </Box>

        <MarkdownEditor />

      </Container>
    </>
  );
};

export default Main;
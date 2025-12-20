import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import { useEffect, useState } from 'react';

import Breadcrumb from "../components/breadcrumbs.jsx";
import EditerHeader from "../components/editer_header.jsx";
import Header from "../components/header.jsx";
import Loading from "../components/loading.jsx";
import MarkdownEditor from "../components/markdowneditor.jsx";
import userStore from "../store/user_store.jsx";
import utils from "../utils/utils.js";

function Main() {
  const { id_token, setTree } = userStore();
  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      var res = utils.requests(
        `${import.meta.env.VITE_API_HOST}/trees`,
        "GET",
        { authorization: `Bearer ${id_token}` },
        {}
      );
      res = await res;

      setTree(res.body.tree);
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
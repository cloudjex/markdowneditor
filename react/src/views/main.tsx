import { Container } from "@mui/material";
import { useEffect } from 'react';

import Editor from "../components/editor";
import Header from "../components/header";
import loadingState from "../store/loading_store";
import userStore from "../store/user_store";
import request_utils from "../utils/request_utils";

import type { TreeResponse } from "../types/types";

function Main() {
  const { id_token, setTree } = userStore();
  const { setLoading } = loadingState();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);

      const res_promise = request_utils.requests<TreeResponse>(
        `${import.meta.env.VITE_API_HOST}/api/trees`,
        "GET",
        { authorization: `Bearer ${id_token}` },
        {}
      );
      const res = await res_promise;

      setTree(res.body.tree);
      setLoading(false);
    };

    if (id_token) {
      fetchData();
    };
  }, []);

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
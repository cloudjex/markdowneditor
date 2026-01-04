import { Box } from "@mui/material";
import { useState, useMemo, useEffect } from "react";
import { useLocation } from "react-router-dom";
import SimpleMde from "react-simplemde-editor";

import "easymde/dist/easymde.min.css";
import "../css/editor.css";
import Breadcrumb from "../components/breadcrumbs";
import EditorHeader from "../components/editor_header";
import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import request_utils from "../utils/request_utils";

import type { NodeResponse } from "../types/types";

export const Editor = () => {
  const { id_token } = userStore();
  const { setLoading } = loadingState();

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('node_id');

  const [markdownValue, setMarkdownValue] = useState<string>("");

  useEffect(() => {
    const fetchNode = async () => {
      setLoading(true);

      const res = await request_utils.requests<NodeResponse>(
        `${import.meta.env.VITE_API_HOST}/api/nodes`,
        "GET",
        { authorization: `Bearer ${id_token}` },
        { node_id: url_node_id }
      );

      let text = "";
      if (res.status == 200) {
        text = res.body.node.text;
      };
      setMarkdownValue(text);

      setLoading(false);
    };

    fetchNode();
  }, [url_node_id]);

  const options = useMemo(() => ({
    spellChecker: false,
    autofocus: true,
    placeholder: "",
    lineNumbers: true,
  }), []);

  return (
    <>
      <Box display="flex" justifyContent="space-between">
        <Breadcrumb />
        <EditorHeader markdownValue={markdownValue} />
      </Box>

      <SimpleMde
        id="simple-mde"
        value={markdownValue}
        onChange={setMarkdownValue}
        options={options}
      />
    </>
  );
};

export default Editor;
import { Box } from "@mui/material";
import { useState, useMemo, useEffect } from "react";
import { useLocation } from "react-router-dom";
import SimpleMde from "react-simplemde-editor";

import "easymde/dist/easymde.min.css";
import "../../css/editor.css";
import RequestHandler from "../../lib/request_handler";
import loadingState from "../../store/loading_store";
import userStore from '../../store/user_store';

import Breadcrumb from "./breadcrumbs";
import EditorHeader from "./editor_header";

import type { NodeResponse } from "../../lib/types";
import type { Options } from "easymde";

function Editor() {
  const { id_token, node_tree } = userStore();
  const { setLoading } = loadingState();
  const [markdownValue, setMarkdownValue] = useState("");

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('id') || "";

  const requests = new RequestHandler(id_token);

  useEffect(() => {
    const fetchNode = async () => {
      setLoading(true);

      const res_promise = requests.get<NodeResponse>(
        `${import.meta.env.VITE_API_HOST}/api/nodes`,
        { id: url_node_id }
      );
      const res = await res_promise;

      setMarkdownValue(res.body.node.text);
      setLoading(false);
    };

    fetchNode();
  }, [url_node_id]);

  const options: Options = useMemo(() => ({
    spellChecker: false,
    autofocus: true,
    placeholder: "",
    lineNumbers: true,
    sideBySideFullscreen: false,
    toolbar: false
  }), []);

  if (!url_node_id) {
    return null;
  }

  return (
    <>
      <Box display="flex" justifyContent="space-between">
        <Breadcrumb node_id={url_node_id} node_tree={node_tree} />
        <EditorHeader node_id={url_node_id} node_tree={node_tree} markdown={markdownValue} />
      </Box>

      <SimpleMde
        value={markdownValue}
        onChange={setMarkdownValue}
        options={options}
      />
    </>
  );
};

export default Editor;
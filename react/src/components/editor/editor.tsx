import { Box } from "@mui/material";
import { useState, useMemo, useEffect } from "react";
import { useParams } from "react-router-dom";
import SimpleMde from "react-simplemde-editor";

import "easymde/dist/easymde.min.css";
import "@/src/css/editor.css";
import type { Node } from "@/src/lib/types";
import type { Options } from "easymde";

import Breadcrumb from "@/src/components/editor/breadcrumbs";
import EditorHeader from "@/src/components/editor/editor_header";
import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Editor() {
  const { id_token, tree } = userStore();
  const { setLoading } = loadingState();
  const [markdownValue, setMarkdownValue] = useState("");

  const urlParams = useParams<{ id: string }>();
  const url_node_id = urlParams.id || "";

  const requests = new RequestHandler(id_token);

  useEffect(() => {
    const fetchNode = async () => {
      setLoading(true);

      const res = await requests.get<Node>(
        `${import.meta.env.VITE_API_HOST}/api/nodes/${url_node_id}`,
      );

      setMarkdownValue(res.body.text);
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
        <Breadcrumb node_id={url_node_id} tree={tree} />
        <EditorHeader node_id={url_node_id} tree={tree} text={markdownValue} />
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
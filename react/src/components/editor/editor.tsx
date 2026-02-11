import { Box } from "@mui/material";
import { useState, useMemo, useEffect } from "react";
import SimpleMde from "react-simplemde-editor";

import "easymde/dist/easymde.min.css";
import "@/src/css/editor.css";
import type { Node, Tree } from "@/src/lib/types";
import type { Options } from "easymde";

import Breadcrumb from "@/src/components/editor/breadcrumbs";
import EditorHeader from "@/src/components/editor/editor_header";
import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Editor(props: { tree: Tree, node_id: string }) {
  const { id_token } = userStore();
  const { setLoading } = loadingState();
  const [markdownValue, setMarkdownValue] = useState("");

  const requests = new RequestHandler(id_token);

  useEffect(() => {
    const fetchNode = async () => {
      setLoading(true);

      const res = await requests.get<Node>(
        `/api/nodes/${props.node_id}`,
      );

      setMarkdownValue(res.body.text);
      setLoading(false);
    };

    fetchNode();
  }, [props.node_id]);

  const options: Options = useMemo(() => ({
    spellChecker: false,
    autofocus: true,
    placeholder: "",
    lineNumbers: true,
    sideBySideFullscreen: false,
    toolbar: false
  }), []);

  return (
    <>
      <Box display="flex" justifyContent="space-between">
        <Breadcrumb node_id={props.node_id} tree={props.tree} />
        <EditorHeader node_id={props.node_id} tree={props.tree} text={markdownValue} />
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

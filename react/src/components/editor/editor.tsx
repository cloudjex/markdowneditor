import "easymde/dist/easymde.min.css";
import "@/css/editor.css";

import { Box } from "@mui/material";
import type { Options } from "easymde";
import { useEffect, useMemo, useState } from "react";
import SimpleMde from "react-simplemde-editor";

import Breadcrumb from "@/components/editor/breadcrumbs";
import EditorHeader from "@/components/editor/editor_header";
import RequestHandler from "@/lib/request_handler";
import type { Node, Tree } from "@/lib/types";
import loadingState from "@/store/loading_store";
import userStore from '@/store/user_store';


function Editor(props: { tree: Tree, nodeId: string }) {
  const { idToken } = userStore();
  const { setLoading } = loadingState();
  const [markdownValue, setMarkdownValue] = useState("");

  const requests = new RequestHandler(idToken);

  useEffect(() => {
    const fetchNode = async () => {
      setLoading(true);

      const res = await requests.get<Node>(
        `/api/nodes/${props.nodeId}`,
      );

      setMarkdownValue(res.body.text);
      setLoading(false);
    };

    fetchNode();
  }, [props.nodeId]);

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
        <Breadcrumb tree={props.tree} nodeId={props.nodeId} />
        <EditorHeader tree={props.tree} nodeId={props.nodeId} text={markdownValue} />
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

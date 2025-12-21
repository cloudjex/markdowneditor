import Box from "@mui/material/Box";
import { useState, useMemo } from "react";
import SimpleMde from "react-simplemde-editor";
import "easymde/dist/easymde.min.css";
import "../css/editor.css";

import Breadcrumb from "../components/breadcrumbs";
import EditorHeader from "../components/editor_header";

export const Editor = () => {
  const [markdownValue, setMarkdownValue] = useState("");

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
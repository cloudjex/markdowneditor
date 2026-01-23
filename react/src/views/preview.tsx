import { Box } from "@mui/material";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { useLocation } from "react-router-dom";
import rehypeAutoLintHeading from "rehype-autolink-headings";
import rehypeHighlight from "rehype-highlight";
import rehypeSlug from "rehype-slug";
import remarkEmoji from "remark-emoji";
import remarkGmf from "remark-gfm";

import "highlight.js/styles/github-dark.css";
import "../css/preview.css";
import RequestHandler from "../lib/request_handler";
import loadingState from "../store/loading_store";
import userStore from "../store/user_store";

import type { NodeResponse } from "../lib/types";

export default function Preview() {
  const { id_token, preview_text } = userStore();
  const { setLoading } = loadingState();

  const location = useLocation();
  const [previewText, setPreviewText] = useState("");

  const requests = new RequestHandler(id_token);
  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('id') || "";

  useEffect(() => {
    async function fetchPreview() {
      if (url_node_id === "local") {
        setPreviewText(preview_text);
        return;
      }

      setLoading(true);

      const res_promise = requests.get<NodeResponse>(
        `${import.meta.env.VITE_API_HOST}/api/nodes`,
        { id: url_node_id }
      );
      const res = await res_promise;

      setLoading(false);
      setPreviewText(res.body.node.text);
    };

    fetchPreview();
  }, [url_node_id]);

  return (
    <>
      <title>Preview</title>

      <Box
        id="preview"
        sx={(theme) => ({
          border: "1px solid #ddd",
          borderRadius: 3,
          px: 5,
          py: 2,
          mx: 7,
          my: 5,

          [theme.breakpoints.down("sm")]: {
            border: 'none',
            px: 1,
            py: 1,
            mx: 1,
            my: 1,
          }
        })}
      >
        <ReactMarkdown
          rehypePlugins={[
            rehypeHighlight,
            rehypeSlug,
            [
              rehypeAutoLintHeading, {
                behavior: "prepend", content: () => ({
                  type: "element",
                  tagName: "span",
                  properties: { className: ["heading-anchor"] },
                  children: [{ type: "text", value: "#" }],
                })
              }
            ],
          ]}
          remarkPlugins={[remarkGmf, remarkEmoji]}
        >
          {previewText}
        </ReactMarkdown>
      </Box >
    </>
  );
}

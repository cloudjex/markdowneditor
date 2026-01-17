import { Box } from "@mui/material";
import { useEffect } from "react";
import ReactMarkdown from "react-markdown";
import rehypeAutoLintHeading from "rehype-autolink-headings";
import rehypeHighlight from "rehype-highlight";
import rehypeSlug from "rehype-slug";
import remarkEmoji from "remark-emoji";
import remarkGmf from "remark-gfm";

import "highlight.js/styles/github-dark.css";
import "../css/preview.css";
import userStore from "../store/user_store";

export default function Preview() {
  const { preview_text } = userStore();

  useEffect(() => {
    const hash = window.location.hash;
    if (hash) {
      const id = hash.replace("#", "");
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: "smooth" });
      }
    }
  }, [preview_text]);

  return (
    <>
      <title>Preview</title>

      <Box sx={(theme) => ({
        border: "1px solid #ddd",
        borderRadius: "8px",
        px: "30px",
        py: "10px",
        mx: "40px",
        my: "10px",

        [theme.breakpoints.down("sm")]: {
          border: 'none',
          px: "2px",
          py: "1px",
          mx: "5px",
          my: "1px",
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
          {preview_text}
        </ReactMarkdown>
      </Box >
    </>
  );
}

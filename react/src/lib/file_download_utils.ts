/**
 * Utility functions for file download using native Web APIs.
 */

/**
 * Escapes special HTML characters in a string.
 */
export function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Creates a temporary anchor element, triggers a download, and cleans up.
 */
function createDownloadLink(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
}

/**
 * Downloads content as a plain text file.
 */
export function downloadAsText(content: string, filename: string): void {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  createDownloadLink(blob, filename);
}

/**
 * Downloads content as a JSON file.
 */
export function downloadAsJson(content: object, filename: string): void {
  const blob = new Blob([JSON.stringify(content, null, 2)], {
    type: "application/json;charset=utf-8",
  });
  createDownloadLink(blob, filename);
}

/**
 * Downloads content as a Markdown file.
 */
export function downloadAsMarkdown(content: string, filename: string): void {
  const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
  const safeFilename = filename.endsWith(".md") ? filename : `${filename}.md`;
  createDownloadLink(blob, safeFilename);
}

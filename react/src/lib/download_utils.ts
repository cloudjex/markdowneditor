class DownloadUtils {
  createDownloadLink(filename: string, blob: Blob): void {
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
    URL.revokeObjectURL(url);
  };

  writeMd(filename: string, content: string): void {
    const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
    this.createDownloadLink(filename, blob);
  }
}

export default DownloadUtils;

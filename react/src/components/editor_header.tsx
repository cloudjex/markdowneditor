import { Box, Button } from '@mui/material';
import fileDownload from 'js-file-download';
import { useLocation } from 'react-router-dom';

import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import request_utils from "../utils/request_utils";
import tree_utils from '../utils/tree_utils';

function EditorHeader(props: { markdownValue: string }) {
  const markdownValue = props.markdownValue;
  const location = useLocation();

  const { id_token, node_tree, setPreviewText } = userStore();
  const { setLoading } = loadingState();

  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('id') || "";

  function preview() {
    setPreviewText(markdownValue);
    window.open(`/preview?id=local`, '_blank');
  };

  function download() {
    const node = tree_utils.get_node(node_tree, url_node_id);
    if (!node) {
      throw new Error(`node is null`);
    }
    const label = node.label;
    fileDownload(markdownValue, `${label}.md`);
  };

  async function upload() {
    setLoading(true);

    const res_promise = request_utils.requests(
      `${import.meta.env.VITE_API_HOST}/api/nodes`,
      "PUT",
      { authorization: `Bearer ${id_token}` },
      { id: url_node_id, text: markdownValue }
    );
    await res_promise;

    setLoading(false);
  };

  return (
    <>
      <Box
        sx={{ mb: 1 }}
      >
        <Button
          variant='outlined'
          size='small'
          onClick={preview}
        >
          プレビュー
        </Button>

        <Button
          variant='outlined'
          size='small'
          sx={{ ml: 1 }}
          onClick={download}
        >
          ファイル取得
        </Button>

        <Button
          variant='outlined'
          size='small'
          sx={{ ml: 1 }}
          onClick={upload}
        >
          保存
        </Button>
      </Box>
    </>
  );
}

export default EditorHeader;
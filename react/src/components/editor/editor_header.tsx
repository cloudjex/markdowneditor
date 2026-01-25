import { Box, Button } from '@mui/material';
import fileDownload from 'js-file-download';

import type { Tree } from '@/src/lib/types';

import RequestHandler from "@/src/lib/request_handler";
import TreeHandler from '@/src/lib/tree_handler';
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function EditorHeader(props: { node_id: string, tree: Tree, markdown: string }) {
  const { id_token, setPreviewText } = userStore();
  const { setLoading } = loadingState();

  const requests = new RequestHandler(id_token);
  const tree_handler = new TreeHandler(props.tree);
  const label = tree_handler.getNode(props.node_id)?.label;

  async function upload() {
    setLoading(true);

    const res_promise = requests.put(
      `${import.meta.env.VITE_API_HOST}/api/nodes/${props.node_id}`,
      { text: props.markdown }
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
          onClick={() => {
            setPreviewText(props.markdown);
            window.open("/preview/state", '_blank');
          }}
        >
          プレビュー
        </Button>

        <Button
          variant='outlined'
          size='small'
          sx={{ ml: 1 }}
          onClick={() => {
            fileDownload(props.markdown, `${label}.md`);
          }}
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
import CloudUploadOutlinedIcon from '@mui/icons-material/CloudUploadOutlined';
import SaveAltOutlinedIcon from '@mui/icons-material/SaveAltOutlined';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import "../css/editor_header.css";
import fileDownload from 'js-file-download';
import { useLocation } from 'react-router-dom';

import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import utils from "../utils/utils";

function EditorHeader(props: { markdownValue: string }) {
  const markdownValue = props.markdownValue;
  const location = useLocation();

  const { id_token } = userStore();
  const { setLoading } = loadingState();

  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('node_id') as string;

  function download() {
    const file_name = url_node_id.split("/").pop();
    fileDownload(markdownValue, `${file_name}.md`);
  };

  async function upload() {
    setLoading(true);

    const res_promise = utils.requests(
      `${import.meta.env.VITE_API_HOST}/nodes`,
      "PUT",
      { authorization: `Bearer ${id_token}` },
      { node_id: url_node_id, text: markdownValue }
    );
    await res_promise;

    setLoading(false);
  };

  return (
    <>
      <Box sx={{ mb: 1, mr: 3 }}>
        <IconButton id="download" sx={{ ml: 1 }} onClick={download}>
          <SaveAltOutlinedIcon />
        </IconButton>

        <IconButton id="save" sx={{ ml: 1 }} onClick={upload}>
          <CloudUploadOutlinedIcon />
        </IconButton>
      </Box>
    </>
  );
}

export default EditorHeader;
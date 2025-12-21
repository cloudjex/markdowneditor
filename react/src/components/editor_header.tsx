import CloudUploadOutlinedIcon from '@mui/icons-material/CloudUploadOutlined';
import SaveAltOutlinedIcon from '@mui/icons-material/SaveAltOutlined';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import "../css/editor_header.css";

function EditorHeader(props: { markdownValue: string }) {
  const markdownValue = props.markdownValue;

  function download() {
    console.log("clicked download");
    console.log(markdownValue);
  };

  function upload() {
    console.log("clicked upload");
    console.log(markdownValue);
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
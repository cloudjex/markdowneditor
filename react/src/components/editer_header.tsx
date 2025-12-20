import SaveOutlinedIcon from '@mui/icons-material/SaveOutlined';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';

function EditerHeader() {
  return (
    <>
      <Box sx={{ mb: 1 }}>
        <IconButton sx={{ ml: 1 }}>
          <SaveOutlinedIcon />
        </IconButton>
      </Box>
    </>
  );
}

export default EditerHeader;
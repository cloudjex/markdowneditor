import MenuIcon from '@mui/icons-material/Menu';
import { Container, Drawer, IconButton, Tooltip, Typography } from '@mui/material';
import { useState } from 'react';
import { useParams } from 'react-router-dom';


import Explorer from '@/src/components/side_bar/explorer';
import TreeUpdate from '@/src/components/side_bar/tree_update';
import userStore from '@/src/store/user_store';


function Sidebar() {
  const urlParams = useParams<{ id: string }>();
  const url_node_id = urlParams.id || "";

  const { tree } = userStore();
  const [drawewrOpen, setDrawerOpen] = useState(false);

  return (
    <>
      <IconButton
        color="inherit"
        size='large'
        edge="start"
        onClick={() => {
          setDrawerOpen((prevState) => !prevState);
        }}
      >
        <Tooltip title="Menu">
          <MenuIcon
            sx={{ fontSize: 30 }}
          />
        </Tooltip>
      </IconButton>

      <Drawer
        open={drawewrOpen}
        onClose={(_, reason) => {
          if (reason === 'backdropClick') {
            setDrawerOpen(false);
          }
        }}
        sx={{
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 300 },
        }}
      >

        <Container sx={{ textAlign: 'left' }}>

          <Typography variant="h5" sx={{ mt: 2 }}>
            Explorer
          </Typography>

          <TreeUpdate node_id={url_node_id} tree={tree} />
          <Explorer node_id={url_node_id} tree={tree} />

        </Container>
      </Drawer >
    </>
  );
}

export default Sidebar;